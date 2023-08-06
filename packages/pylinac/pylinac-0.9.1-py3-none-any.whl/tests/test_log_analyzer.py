import os
from unittest import TestCase
import time
import os.path as osp

from pylinac.log_analyzer import MachineLog, MachineLogs, log_types

from tests.utils import save_file


class TestLogLoading(TestCase):
    """Tests of dynalog files, mostly using the demo file."""
    test_dir = osp.join(osp.dirname(__file__), 'test_files', 'MLC logs')

    def test_loading(self):
        """Test that loading the badly-named dynalog still loads and identifies properly."""
        test_tlog = osp.join(self.test_dir, 'tlogs', "qqq2106_4DC Treatment_JS0_TX_20140712095629.bin")
        # should produce no errors
        # load method 1
        MachineLog(test_tlog)
        # load method 2
        log = MachineLog()
        self.assertFalse(log.is_loaded)
        log.load(test_tlog)
        self.assertTrue(log.is_loaded)

        # throw an error for files that aren't logs
        not_a_file = test_tlog.replace(".bin", 'blahblah.bin')
        self.assertRaises(FileExistsError, MachineLog, not_a_file)
        not_a_log = osp.join(osp.dirname(__file__), 'test_files', 'VMAT', 'DRGSmlc-105-example.dcm')
        self.assertRaises(IOError, MachineLog, not_a_log)

    def test_dynalog_loading(self):
        a_file = osp.join(self.test_dir, 'dlogs', 'Adlog1.dlg')
        MachineLog(a_file)

        b_file = osp.join(self.test_dir, 'dlogs', 'Bdlog1.dlg')
        MachineLog(b_file)

        a_but_not_b_dir = osp.join(self.test_dir, 'a_no_b_dir', 'Adlog1.dlg')
        self.assertRaises(FileNotFoundError, MachineLog, a_but_not_b_dir)
        b_but_not_a_dir = osp.join(self.test_dir, 'b_no_a_dir', 'Bdlog1.dlg')
        self.assertRaises(FileNotFoundError, MachineLog, b_but_not_a_dir)

        bad_name_dlg = osp.join(self.test_dir, 'bad_names', 'bad_name_dlg.dlg')
        self.assertRaises(ValueError, MachineLog, bad_name_dlg)

    def test_txt_file_also_loads_if_around(self):
        # has a .txt file
        log_with_txt = osp.join(self.test_dir, 'SG TB1 MLC', "qqq2106_4DC Treatment_JST90_TX_20140712094246.bin")

        log = MachineLog(log_with_txt)
        self.assertTrue(hasattr(log, 'txt'))
        self.assertIsInstance(log.txt, dict)
        self.assertEqual(log.txt['Patient ID'], 'qqq2106')

        # DOESN'T have a txt file
        log_no_txt = osp.join(self.test_dir, 'tlogs', "qqq2106_4DC Treatment_JS0_TX_20140712095629.bin")

        log = MachineLog(log_no_txt)
        self.assertFalse(hasattr(log, 'txt'))

    def test_from_url(self):
        url = 'https://s3.amazonaws.com/assuranceqa-staging/uploads/imgs/Tlog2.bin'
        log = MachineLog.from_url(url)


class TestDynalogDemo(TestCase):
    """Tests having to do with trajectory log files."""
    @classmethod
    def setUpClass(cls):
        cls.log = MachineLog()
        cls.log.load_demo_dynalog()

    def test_type(self):
        """Test all kinds of things about the dynalog demo."""
        self.assertTrue(self.log.log_type == log_types['dlog'])

    def test_header(self):
        """Test header info of the dynalog; ensures data integrity."""
        header = self.log.header
        self.assertEqual(header.version, 'B')
        self.assertEqual(header.patient_name, ['Clinac4 QA', '', 'Clinac4 QA'])
        self.assertEqual(header.plan_filename, ['1.2.246.352.71.5.1399119341.107477.20110923193623', '21'])
        self.assertEqual(header.tolerance, 102)
        self.assertEqual(header.num_mlc_leaves, 120)
        self.assertEqual(header.clinac_scale, 1)

    def test_axis_data(self):
        """Sample a few points from the axis data to ensure integrity."""
        axis_data = self.log.axis_data
        # properties
        self.assertEqual(axis_data.num_beamholds, 20)
        self.assertEqual(axis_data.num_snapshots, 99)
        self.assertEqual(len(axis_data.beam_hold.actual), 99)
        # MU data
        self.assertEqual(axis_data.mu.actual[0], 0)
        self.assertEqual(axis_data.mu.actual[-1], 25000)
        self.assertEqual(axis_data.mu.expected[0], 0)
        self.assertEqual(axis_data.mu.expected[-1], 25000)
        # jaws
        self.assertEqual(axis_data.jaws.x1.actual[0], 8)
        self.assertEqual(axis_data.jaws.y1.actual[-1], 20)
        self.assertRaises(AttributeError, axis_data.jaws.x2.plot_expected)

    def test_mlc(self):
        """Test integrity of MLC data & methods."""
        mlc = self.log.axis_data.mlc
        self.assertEqual(mlc.num_leaves, 120)
        self.assertEqual(mlc.num_pairs, 60)
        self.assertEqual(mlc.num_snapshots, 21)  # snapshots where beam was on
        self.assertEqual(len(mlc.moving_leaves), 60)
        self.assertFalse(mlc.hdmlc)

    def test_mlc_positions(self):
        """Test some MLC positions."""
        mlc = self.log.axis_data.mlc
        self.assertAlmostEqual(mlc.leaf_axes[1].actual[0], 7.564, delta=0.001)
        self.assertAlmostEqual(mlc.leaf_axes[120].expected[-1], -4.994, delta=0.001)
        self.assertAlmostEqual(mlc.leaf_axes[1].difference[0], 0, delta=0.1)

    def test_mlc_leafpair_moved(self):
        mlc = self.log.axis_data.mlc
        self.assertTrue(mlc.leaf_moved(9))
        self.assertFalse(mlc.leaf_moved(8))
        self.assertTrue(mlc.pair_moved(3))

    def test_RMS_error(self):
        mlc = self.log.axis_data.mlc
        self.assertAlmostEqual(mlc.get_RMS_avg(), 0.0373, delta=0.001)
        self.assertAlmostEqual(mlc.get_RMS_avg(bank='a'), 0.0375, delta=0.001)
        self.assertAlmostEqual(mlc.get_RMS_avg(only_moving_leaves=True), 0.074, delta=0.01)
        self.assertAlmostEqual(mlc.get_RMS_max(), 0.0756, delta=0.001)
        self.assertAlmostEqual(mlc.get_RMS_percentile(), 0.0754, delta=0.001)
        self.assertAlmostEqual(len(mlc.get_RMS('b')), 60)
        self.assertAlmostEqual(mlc.get_RMS((1,3)).mean(), 0.0717, delta=0.001)
        self.assertAlmostEqual(mlc.create_error_array((2,3), False).mean(), 0.034, delta=0.001)

    def test_under_jaws(self):
        mlc = self.log.axis_data.mlc
        self.assertFalse(mlc.leaf_under_y_jaw(4))

    def test_save_to_csv(self):
        # should raise error since it's a dynalog
        with self.assertRaises(TypeError):
            self.log.to_csv('test.csv')

    def test_plot_all(self):
        with self.assertRaises(AttributeError):
            self.log.plot_all()

        self.log.fluence.gamma.calc_map()
        self.log.plot_all()

    def test_treatment_type(self):
        self.assertEqual(self.log.treatment_type, 'Dynamic IMRT')

    def test_axis_moved(self):
        self.assertFalse(self.log.axis_data.gantry.moved)
        self.assertTrue(self.log.axis_data.mlc.leaf_axes[35].moved)


class TestDlogFluence(TestCase):

    def setUp(self):
        self.log = MachineLog()
        self.log.load_demo_dynalog()

    def test_demo(self):
        self.log.run_dlog_demo()

    def test_fluence(self):
        fluence = self.log.fluence

        self.assertFalse(fluence.actual.map_calced)
        self.assertFalse(fluence.expected.map_calced)
        self.assertFalse(fluence.gamma.map_calced)
        self.assertRaises(AttributeError, fluence.actual.plot_map)

        # do repeating fluence calcs; ensure semi-lazy property
        start = time.time()
        fluence.actual.calc_map()
        end = time.time()
        first_calc_time = end - start
        start = time.time()
        fluence.actual.calc_map()
        end = time.time()
        second_calc_time = end - start
        self.assertLess(second_calc_time, first_calc_time)

        # same for gamma
        start = time.time()
        fluence.gamma.calc_map(resolution=0.15)
        end = time.time()
        first_calc_time = end - start
        start = time.time()
        fluence.gamma.calc_map(resolution=0.15)
        end = time.time()
        second_calc_time = end - start
        self.assertLess(second_calc_time, first_calc_time)

        self.assertAlmostEqual(fluence.gamma.pass_prcnt, 99.85, delta=0.1)
        self.assertAlmostEqual(fluence.gamma.avg_gamma, 0.019, delta=0.005)
        self.assertAlmostEqual(fluence.gamma.histogram()[0][0], 155804, delta=100)


class TestTlogDemo(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = MachineLog()
        cls.log.load_demo_trajectorylog()

    def test_demo(self):
        MachineLog().run_tlog_demo()

    def test_type(self):
        self.assertTrue(self.log.log_type, log_types['tlog'])

    def test_header(self):
        header = self.log.header
        self.assertEqual(header.header, 'VOSTL')
        self.assertEqual(header.version, 2.1)
        self.assertEqual(header.header_size, 1024)
        self.assertEqual(header.sampling_interval, 20)
        self.assertEqual(header.num_axes, 14)
        self.assertEqual(header.axis_enum.size, 14)
        self.assertEqual(header.samples_per_axis.size, 14)
        self.assertEqual(header.samples_per_axis[-1], 122)
        self.assertEqual(header.num_mlc_leaves, 120)
        self.assertEqual(header.axis_scale, 1)
        self.assertEqual(header.num_subbeams, 2)
        self.assertEqual(header.is_truncated, 0)
        self.assertEqual(header.num_snapshots, 5200)
        self.assertEqual(header.mlc_model, 3)

    def test_axis_data(self):
        axis_data = self.log.axis_data
        self.assertAlmostEqual(axis_data.collimator.actual[0], 180, delta=0.1)
        self.assertAlmostEqual(axis_data.mu.difference[1], 0.0000337, delta=0.01)
        self.assertAlmostEqual(axis_data.gantry.expected[2], 310, delta=0.1)

    def test_mlc(self):
        mlc = self.log.axis_data.mlc
        self.assertTrue(mlc.hdmlc)
        self.assertEqual(mlc.num_leaves, 120)
        self.assertEqual(mlc.num_pairs, 60)
        self.assertEqual(mlc.num_snapshots, 1021)

        log_no_exclusion = MachineLog()
        log_no_exclusion.load_demo_trajectorylog(exclude_beam_off=False)
        self.assertEqual(log_no_exclusion.axis_data.mlc.num_snapshots, 5200)

    def test_under_jaws(self):
        mlc = self.log.axis_data.mlc
        self.assertTrue(mlc.leaf_under_y_jaw(4))

    def test_RMS_error(self):
        mlc = self.log.axis_data.mlc
        self.assertAlmostEqual(mlc.get_RMS_avg(), 0.001, delta=0.001)
        self.assertAlmostEqual(mlc.get_RMS_max(), 0.00216, delta=0.001)
        self.assertAlmostEqual(mlc.get_RMS_percentile(), 0.00196, delta=0.001)

    def test_save_to_csv(self):
        save_file('tester.csv', self.log.to_csv)

        # without filename should make one based off tlog name
        self.log.to_csv()
        time.sleep(0.1)
        name = self.log._filename_str.replace('.bin', '.csv')
        self.assertTrue(osp.isfile(name))
        os.remove(name)
        self.assertFalse(osp.isfile(name))

    def test_plot_axes(self):
        for methodname in ('plot_actual', 'plot_expected', 'plot_difference'):
            method = getattr(self.log.axis_data.gantry, methodname)
            method()

    def test_save_axes(self):
        for methodname in ('save_plot_actual', 'save_plot_expected', 'save_plot_difference'):
            method = getattr(self.log.axis_data.gantry, methodname)
            save_file('test.png', method)


class TestTlogFluence(TestCase):

    def setUp(self):
        self.log = MachineLog()
        self.log.load_demo_trajectorylog()

    def test_fluence(self):
        fluence = self.log.fluence
        fluence.gamma.calc_map()
        self.assertAlmostEqual(fluence.gamma.pass_prcnt, 100, delta=0.1)
        self.assertAlmostEqual(fluence.gamma.avg_gamma, 0.001, delta=0.005)
        self.assertAlmostEqual(fluence.gamma.histogram()[0][0], 240000, delta=100)

    def test_plotting(self):
        # raise error if map hasn't yet been calc'ed.
        with self.assertRaises(AttributeError):
            self.log.fluence.actual.plot_map()

        self.log.fluence.actual.calc_map()
        self.log.fluence.actual.plot_map()

    def test_saving_plots(self):
        self.log.fluence.gamma.calc_map()
        save_file('test.png', self.log.fluence.gamma.save_map)

    def test_subbeam_data(self):
        """Test accessing the subbeam data."""
        expected_vals = [310, 180, 3.7, 3.4, 3.8, 3.9]
        for item, expval in zip(('gantry_angle', 'collimator_angle', 'jaw_x1', 'jaw_x2', 'jaw_y1', 'jaw_y2'), expected_vals):
            val = getattr(self.log.subbeams[0], item)
            self.assertAlmostEqual(val.actual, expval, delta=0.1)


class Test_MachineLogs(TestCase):
    _logs_dir = osp.abspath(osp.join(osp.dirname(__file__), '.', 'test_files', 'MLC logs'))
    logs_dir = osp.join(_logs_dir, 'SG TB1 MLC')
    logs_altdir = osp.join(_logs_dir, 'altdir')
    mix_type_dir = osp.join(_logs_dir, 'mixed_types')

    def test_loading(self):
        # test root level directory
        logs = MachineLogs(self.logs_dir, recursive=False, verbose=True)
        self.assertEqual(logs.num_logs, 7)
        # test recursive
        logs = MachineLogs(self.logs_dir, verbose=False)
        self.assertEqual(logs.num_logs, 8)
        # test using method
        logs = MachineLogs()
        logs.load_folder(self.logs_dir, verbose=False)
        self.assertEqual(logs.num_logs, 8)

    def test_basic_parameters(self):
        # no real test other than to make sure it works
        logs = MachineLogs(self.logs_dir, verbose=False)
        logs.report_basic_parameters()

    def test_num_logs(self):
        logs = MachineLogs(self.logs_dir, recursive=False, verbose=False)
        self.assertEqual(logs.num_logs, 7)
        self.assertEqual(logs.num_tlogs, 7)
        self.assertEqual(logs.num_dlogs, 0)

        logs = MachineLogs(self.mix_type_dir, verbose=False)
        self.assertEqual(logs.num_dlogs, 1)
        self.assertEqual(logs.num_tlogs, 2)

    def test_empty_dir(self):
        empty_dir = osp.join(self._logs_dir, 'empty_dir')
        logs = MachineLogs(empty_dir)
        self.assertEqual(logs.num_logs, 0)

    def test_mixed_types(self):
        """test mixed directory (tlogs & dlogs)"""
        log_dir = osp.join(self._logs_dir, 'mixed_types')
        logs = MachineLogs(log_dir, verbose=False)
        self.assertEqual(logs.num_logs, 3)

    def test_dlog_matches_missing(self):
        """Test that Dlogs without a match are skipped."""
        log_dir = osp.join(self._logs_dir, 'some_matches_missing')
        logs = MachineLogs(log_dir, verbose=False)
        self.assertEqual(logs.num_logs, 1)

    def test_append(self):
        # append a directory
        logs = MachineLogs()
        logs.append(self.logs_altdir)
        self.assertEqual(logs.num_logs, 4)
        # append a file string
        logs = MachineLogs()
        single_file = osp.join(self.logs_altdir, 'qqq2106_4DC Treatment_JST90_TX_20140712094246.bin')
        logs.append(single_file)
        # append a MachineLog
        logs = MachineLogs()
        single_log = MachineLog(single_file)
        logs.append(single_log)

        # try to append something that's not a Log
        log = None
        with self.assertRaises(TypeError):
            logs.append(log)

    def test_empty_op(self):
        """Test that error is raised if trying to do op with no logs."""
        logs = MachineLogs()
        self.assertRaises(ValueError, logs.avg_gamma)

    def test_avg_gamma(self):
        logs = MachineLogs(self.logs_dir, recursive=False, verbose=False)
        gamma = logs.avg_gamma()
        self.assertAlmostEqual(gamma, 0, delta=0.002)

    def test_avg_gamma_pct(self):
        logs = MachineLogs(self.logs_dir, recursive=False, verbose=False)
        for log in logs:
            print(log.header.num_snapshots)
        gamma = logs.avg_gamma_pct()
        self.assertAlmostEqual(gamma, 100, delta=0.01)