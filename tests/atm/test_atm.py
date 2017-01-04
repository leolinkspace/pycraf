#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals

import pytest
import numpy as np
from numpy.testing import assert_equal, assert_allclose
from astropy.tests.helper import assert_quantity_allclose
from astropy import units as apu
from astropy.units import Quantity
from pycraf import conversions as cnv
from pycraf import atm
from pycraf.helpers import check_astro_quantities
# from astropy.utils.misc import NumpyRNGContext


HEIGHTS_PROFILE = [1, 10, 30, 50]

LOW_LATITUDE_PROFILE = (
    [294.074786, 237.4778, 226.929, 270.],
    [9.0662840000e+02, 2.8485260000e+02, 1.5058940282e+01, 7.9610185204e-01],
    [1.4121645413e+01, 5.1420983832e-02, 2.8760293829e-05, 1.2778908988e-06],
    [1.9163912565e+01, 5.6351371086e-02, 3.0117880564e-05, 1.5922037041e-06],
    [1.000321953, 1.0000934535, 1.0000051497, 1.0000002288],
    [7.7328565313e+01, 1.9123515880e+01, 3.0810215083e-02, 3.2822397733e-05],
    [6.3372667216e+01, 2.7109493483e+01, 4.8305812726e-02, 3.3861489334e-05]
    )
MID_LATITUDE_SUMMER_PROFILE = (
    [289.69681, 235.7158, 239.1281161835, 275.],
    [9.0512630000e+02, 2.8370960000e+02, 1.4998514754e+01, 7.9290741247e-01],
    [9.2511658582e+00, 6.1239834071e-02, 2.7183571711e-05, 1.2496220820e-06],
    [1.2367481486e+01, 6.6613735486e-02, 2.9997029508e-05, 1.5858148249e-06],
    [1.0002974576, 1.0000938475, 1.0000048674, 1.0000002238],
    [6.5625276293e+01, 2.6973090572e+01, 8.6514873296e-03, 2.2689790254e-05],
    [5.6042205096e+01, 3.8893128319e+01, 1.2070076105e-02, 2.2300580055e-05]
    )

MID_LATITUDE_WINTER_PROFILE = (
    [268.8965, 218., 218., 265.],
    [8.9939800000e+02, 2.5897870000e+02, 1.3691097703e+01, 7.2378985731e-01],
    [2.5601686537e+00, 5.1486866321e-04, 2.7218907085e-05, 1.1837378270e-06],
    [3.1768361347e+00, 5.1795740000e-04, 2.7382195406e-05, 1.4475797146e-06],
    [1.000275954, 1.000092191, 1.0000048737, 1.000000212],
    [7.1111038308e+01, 1.4804733448e+00, 7.8275883604e-02, 4.3666584179e-05],
    [7.4149819324e+01, 2.5199845271e+00, 1.3323965782e-01, 4.7298325519e-05]
    )

HIGH_LATITUDE_SUMMER_PROFILE = (
    [281.9167, 225., 238.4880972095, 277.],
    [8.9871920000e+02, 2.6961380000e+02, 1.4253330015e+01, 7.5351267819e-01],
    [6.2160419038e+00, 1.9974283742e-02, 2.5902312529e-05, 1.1789617138e-06],
    [8.0867836667e+00, 2.0739334758e-02, 2.8506660030e-05, 1.5070253564e-06],
    [1.000285359, 1.0000931397, 1.000004638, 1.0000002111],
    [7.1489866454e+01, 2.6283360671e+01, 8.7548059357e-03, 1.8709488048e-05],
    [6.5737586877e+01, 4.1958217549e+01, 1.2290245236e-02, 1.8036994890e-05]
    )

HIGH_LATITUDE_WINTER_PROFILE = (
    [258.31873, 217.5, 217.5, 260.],
    [8.9319570000e+02, 2.4387180000e+02, 1.2892460426e+01, 6.8156931564e-01],
    [1.2069272815e+00, 4.8594960055e-04, 2.5690079763e-05, 1.1361236208e-06],
    [1.4387259924e+00, 4.8774360000e-04, 2.5784920851e-05, 1.3631386313e-06],
    [1.0002763674, 1.0000870128, 1.0000046, 1.0000002034],
    [7.4051289792e+01, 1.4808289258e+00, 7.8294183974e-02, 6.1169881534e-05],
    [8.5625388441e+01, 2.5319294785e+00, 1.3387023112e-01, 6.9578758372e-05]
    )


class TestConversions:

    def setup(self):

        pass

    def teardown(self):

        pass

    def test_opacity_from_atten(self):

        args_list = [
            (1.000000000001, None, cnv.dimless),
            (-90, 90, apu.deg),
            ]
        check_astro_quantities(atm.opacity_from_atten, args_list)

        elev = 50 * apu.deg
        atten_dB = Quantity([0.1, 1, 10, 50, 100], cnv.dB)
        opacity = Quantity([
            1.76388252e-02, 0.17638825, 1.76388252, 8.81941258, 17.63882515
            ], cnv.dimless)

        assert_quantity_allclose(
            atm.opacity_from_atten(atten_dB, elev),
            opacity
            )

        assert_quantity_allclose(
            atm.opacity_from_atten(atten_dB.to(cnv.dimless), elev),
            opacity
            )

    def test_atten_from_opacity(self):

        args_list = [
            (0.000000000001, None, cnv.dimless),
            (-90, 90, apu.deg),
            ]
        check_astro_quantities(atm.atten_from_opacity, args_list)

        elev = 50 * apu.deg
        atten_dB = Quantity([0.1, 1, 10, 50, 100], cnv.dB)
        opacity = Quantity([
            1.76388252e-02, 0.17638825, 1.76388252, 8.81941258, 17.63882515
            ], cnv.dimless)

        assert_quantity_allclose(
            atm.atten_from_opacity(opacity, elev),
            atten_dB
            )

    def test_refractive_index(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.hPa),
            (1.e-30, None, apu.hPa),
            ]
        check_astro_quantities(atm.refractive_index, args_list)

        temp = Quantity([100, 200, 300], apu.K)
        press = Quantity([900, 1000, 1100], apu.hPa)
        press_w = Quantity([200, 500, 1000], apu.hPa)

        refr_index = Quantity(
            [1.00816352, 1.0050537, 1.00443182], cnv.dimless
            )

        assert_quantity_allclose(
            atm.refractive_index(temp, press, press_w),
            refr_index
            )
        assert_quantity_allclose(
            atm.refractive_index(
                temp.to(apu.mK), press.to(apu.Pa), press_w.to(apu.Pa)
                ),
            refr_index
            )

    def test_saturation_water_pressure(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.hPa),
            ]
        check_astro_quantities(atm.saturation_water_pressure, args_list)

        temp = Quantity([100, 200, 300], apu.K)
        press = Quantity([900, 1000, 1100], apu.hPa)

        press_w = Quantity(
            [2.53167296e-17, 3.22017860e-03, 3.53919927e+01], apu.hPa
            )

        assert_quantity_allclose(
            atm.saturation_water_pressure(temp, press),
            press_w
            )
        assert_quantity_allclose(
            atm.saturation_water_pressure(
                temp.to(apu.mK), press.to(apu.Pa)
                ),
            press_w
            )

    def test_pressure_water_from_humidity(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.hPa),
            (0, 100, apu.percent),
            ]
        check_astro_quantities(atm.pressure_water_from_humidity, args_list)

        temp = Quantity([280., 290., 295.], apu.K)
        press = Quantity([990., 980., 985.], apu.hPa)
        humid = Quantity(
            [97.6257799244, 34.8273661769, 2.5950905603], apu.percent
            )
        press_w = Quantity(
            [9.6908167974, 6.6912782649, 0.6806645132], apu.hPa
            )

        assert_quantity_allclose(
            atm.pressure_water_from_humidity(temp, press, humid),
            press_w
            )

    def test_humidity_from_pressure_water(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.hPa),
            (1.e-30, None, apu.hPa),
            ]
        check_astro_quantities(atm.humidity_from_pressure_water, args_list)

        temp = Quantity([280., 290., 295.], apu.K)
        press = Quantity([990., 980., 985.], apu.hPa)
        humid = Quantity(
            [97.6257799244, 34.8273661769, 2.5950905603], apu.percent
            )
        press_w = Quantity(
            [9.6908167974, 6.6912782649, 0.6806645132], apu.hPa
            )

        assert_quantity_allclose(
            atm.humidity_from_pressure_water(temp, press, press_w),
            humid
            )

    def test_pressure_water_from_rho_water(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.g / apu.m ** 3),
            ]
        check_astro_quantities(atm.pressure_water_from_rho_water, args_list)

        temp = Quantity([280., 290., 295.], apu.K)
        rho_w = Quantity([7.5, 5., 0.5], apu.g / apu.m ** 3)
        press_w = Quantity(
            [9.6908167974, 6.6912782649, 0.6806645132], apu.hPa
            )

        assert_quantity_allclose(
            atm.pressure_water_from_rho_water(temp, rho_w),
            press_w
            )

    def test_rho_water_from_pressure_water(self):

        args_list = [
            (1.e-30, None, apu.K),
            (1.e-30, None, apu.hPa),
            ]
        check_astro_quantities(atm.rho_water_from_pressure_water, args_list)

        temp = Quantity([280., 290., 295.], apu.K)
        rho_w = Quantity([7.5, 5., 0.5], apu.g / apu.m ** 3)
        press_w = Quantity(
            [9.6908167974, 6.6912782649, 0.6806645132], apu.hPa
            )

        assert_quantity_allclose(
            atm.rho_water_from_pressure_water(temp, press_w),
            rho_w
            )

    def test_standard_profile(self):

        args_list = [
            (0, 84.99999999, apu.km),
            ]
        check_astro_quantities(atm.standard_profile, args_list)

        # also testing multi-dim arrays:
        heights = Quantity([[1, 10], [3, 20], [30, 50]], apu.km)
        (
            temperatures,
            pressures,
            rho_water,
            pressures_water,
            ref_indices,
            humidities_water,
            humidities_ice,
            ) = atm.standard_profile(heights)

        assert_quantity_allclose(
            temperatures,
            Quantity([
                [281.65, 223.15],
                [268.65, 216.65],
                [226.65, 270.65],
                ], apu.K)
            )
        assert_quantity_allclose(
            pressures,
            Quantity([
                [8.98746319e+02, 2.64364701e+02],
                [7.01086918e+02, 5.47497974e+01],
                [1.17189629e+01, 7.59478828e-01]
                ], apu.hPa)
            )
        assert_quantity_allclose(
            rho_water,
            Quantity([
                [4.54897995e+00, 5.05346025e-02],
                [1.67347620e+00, 3.40499473e-04],
                [2.24089942e-05, 1.21617633e-06]
                ], apu.g / apu.m ** 3)
            )
        assert_quantity_allclose(
            pressures_water,
            Quantity([
                [5.91241441e+00, 5.20387473e-02],
                [2.07466258e+00, 3.40420909e-04],
                [2.34379258e-05, 1.51895766e-06]
                ], apu.hPa)
            )
        assert_quantity_allclose(
            ref_indices,
            Quantity([
                [1.00027544, 1.00009232],
                [1.00021324, 1.00001961],
                [1.00000401, 1.00000022]
                ], cnv.dimless)
            )
        assert_quantity_allclose(
            humidities_water,
            Quantity([
                [5.32203441e+01, 8.13127069e+01],
                [4.73130499e+01, 1.14611315e+00],
                [2.47252816e-02, 2.98350935e-05]
                ], apu.percent)
            )
        assert_quantity_allclose(
            humidities_ice,
            Quantity([
                [4.90631621e+01, 1.32054502e+02],
                [4.94539968e+01, 1.97460163e+00],
                [3.88672315e-02, 3.05857984e-05]
                ], apu.percent)
            )

    def test_special_profiles(self):

        for _profile_name in [
                'low_latitude_profile',
                'mid_latitude_summer_profile', 'mid_latitude_winter_profile',
                'high_latitude_summer_profile', 'high_latitude_winter_profile'
                ]:

            _prof_func = getattr(atm, _profile_name)
            heights = Quantity(HEIGHTS_PROFILE, apu.km)
            consts = globals()[_profile_name.upper()]

            print(_profile_name, consts)
            (
                c_temperatures,
                c_pressures,
                c_rho_water,
                c_pressures_water,
                c_ref_indices,
                c_humidities_water,
                c_humidities_ice,
                ) = consts

            with pytest.raises(TypeError):
                _prof_func(50)

            with pytest.raises(apu.UnitsError):
                _prof_func(50 * apu.Hz)

            with pytest.raises(AssertionError):
                _prof_func(-1 * apu.km)

            with pytest.raises(AssertionError):
                _prof_func(101 * apu.km)

            (
                temperatures,
                pressures,
                rho_water,
                pressures_water,
                ref_indices,
                humidities_water,
                humidities_ice,
                ) = _prof_func(heights)

            assert_quantity_allclose(
                temperatures,
                Quantity(c_temperatures, apu.K)
                )
            assert_quantity_allclose(
                pressures,
                Quantity(c_pressures, apu.hPa)
                )
            assert_quantity_allclose(
                rho_water,
                Quantity(c_rho_water, apu.g / apu.m ** 3)
                )
            assert_quantity_allclose(
                pressures_water,
                Quantity(c_pressures_water, apu.hPa)
                )
            assert_quantity_allclose(
                ref_indices,
                Quantity(c_ref_indices, cnv.dimless)
                )
            assert_quantity_allclose(
                humidities_water,
                Quantity(c_humidities_water, apu.percent)
                )
            assert_quantity_allclose(
                humidities_ice,
                Quantity(c_humidities_ice, apu.percent)
                )

    def test_specific_attenuation_annex1(self):

        args_list = [
            (1.e-30, None, apu.GHz),
            (1.e-30, None, apu.hPa),
            (1.e-30, None, apu.hPa),
            (1.e-30, None, apu.K),
            ]
        check_astro_quantities(atm.specific_attenuation_annex1, args_list)

        # test for scalar quantities
        with pytest.raises(TypeError):
            atm.specific_attenuation_annex1(
                1 * apu.GHz,
                Quantity([1000, 1000], apu.hPa),
                10 * apu.hPa, 300 * apu.K
                )

        with pytest.raises(TypeError):
            atm.specific_attenuation_annex1(
                1 * apu.GHz, 1000 * apu.hPa,
                Quantity([10, 10], apu.hPa),
                300 * apu.K
                )

        with pytest.raises(TypeError):
            atm.specific_attenuation_annex1(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.hPa,
                Quantity([300, 300], apu.K)
                )
        atten_dry, atten_wet = atm.specific_attenuation_annex1(
            np.logspace(1, 2, 5) * apu.GHz,
            980 * apu.hPa,
            10 * apu.hPa,
            300 * apu.K
            )

        assert_quantity_allclose(
            atten_dry,
            Quantity([
                6.8734000906e-03, 8.9691079865e-03, 2.0108798019e-02,
                7.0886935962e+00, 2.6981301299e-02
                ], cnv.dB / apu.km)
            )

        assert_quantity_allclose(
            atten_wet,
            Quantity([
                0.0057314491, 0.0425094528, 0.0665904646, 0.1297056177,
                0.3999561273
                ], cnv.dB / apu.km)
            )

    def test_terrestrial_attenuation(self):

        args_list = [
            (1.e-30, None, cnv.dB / apu.km),
            (1.e-30, None, apu.km),
            ]
        check_astro_quantities(atm.terrestrial_attenuation, args_list)

        assert_quantity_allclose(
            atm.terrestrial_attenuation(
                Quantity([
                    0.0057314491, 0.0425094528, 0.0665904646, 0.1297056177
                    ], cnv.dB / apu.km),
                Quantity(10, apu.km),
                ),
            Quantity([
                0.057314491, 0.425094528, 0.665904646, 1.297056177
                ], cnv.dB)
            )

    def test_slant_attenuation_annex1(self):

        # from functools import partial
        # _func = partial(
        #     atm.slant_attenuation_annex1,
        #     profile_func=atm.standard_profile
        #     )

        # args_list = [
        #     (1.e-30, None, apu.GHz),
        #     (-90, 90, apu.deg),
        #     (1.e-30, None, apu.m),
        #     (1.e-30, None, apu.K),
        #     (1.e-30, None, apu.km),
        #     ]
        # check_astro_quantities(_func, args_list)

        atten, refract, tebb = atm.slant_attenuation_annex1(
            np.logspace(1, 2, 5) * apu.GHz, 30 * apu.deg, 400 * apu.m,
            atm.standard_profile,
            )

        assert_quantity_allclose(
            atten,
            Quantity([
                1.0279145660e-01, 2.6893903556e-01, 4.9024818093e-01,
                1.5542565085e+02, 1.8943476778e+00
                ], cnv.dB)
            )

        assert_quantity_allclose(
            refract, Quantity(-0.03139592908582769, apu.deg)
            )

        assert_quantity_allclose(
            tebb,
            Quantity([
                8.8560899728, 18.8378849911, 31.25205135,
                286.3083466743, 99.2258260009
                ], apu.K)
            )

    def test_specific_attenuation_annex2(self):

        # first test, if assert Quantity works
        with pytest.raises(TypeError):
            atm.specific_attenuation_annex2(
                1, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(TypeError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(TypeError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10, 300 * apu.K
                )

        with pytest.raises(TypeError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300
                )

        with pytest.raises(apu.UnitsError):
            atm.specific_attenuation_annex2(
                1 * apu.m, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(apu.UnitsError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.m, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(apu.UnitsError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.m, 300 * apu.K
                )

        with pytest.raises(apu.UnitsError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300 * apu.m
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                -1 * apu.GHz, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, -1000 * apu.hPa, 10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, -10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3, -300 * apu.K
                )

        # test for scalar quantities
        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz,
                Quantity([1000, 1000], apu.hPa),
                10 * apu.g / apu.m ** 3, 300 * apu.K
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa,
                Quantity([10, 10], apu.g / apu.m ** 3),
                300 * apu.K
                )

        with pytest.raises(AssertionError):
            atm.specific_attenuation_annex2(
                1 * apu.GHz, 1000 * apu.hPa, 10 * apu.g / apu.m ** 3,
                Quantity([300, 300], apu.K)
                )
        atten_dry, atten_wet = atm.specific_attenuation_annex2(
            np.logspace(1, 2, 5) * apu.GHz,
            980 * apu.hPa,
            10 * apu.g / apu.m ** 3,
            300 * apu.K
            )

        assert_quantity_allclose(
            atten_dry,
            Quantity([
                0.006643591, 0.008556794, 0.0200009175, 6.5824558517,
                0.0215553521
                ], cnv.dB / apu.km)
            )

        assert_quantity_allclose(
            atten_wet,
            Quantity([
                0.0082768112, 0.0599180804, 0.096043373, 0.1902800424,
                0.5888230557
                ], cnv.dB / apu.km)
            )

    def test_slant_attenuation_annex2(self):

        # first test, if assert Quantity works
        with pytest.raises(TypeError):
            atm.slant_attenuation_annex2(
                1, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(TypeError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(TypeError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(TypeError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1, 30 * apu.deg
                )

        with pytest.raises(TypeError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30
                )

        with pytest.raises(apu.UnitsError):
            atm.slant_attenuation_annex2(
                1 * apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(apu.UnitsError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(apu.UnitsError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.s, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(apu.UnitsError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.s, 30 * apu.deg
                )

        with pytest.raises(apu.UnitsError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.s
                )

        with pytest.raises(AssertionError):
            atm.slant_attenuation_annex2(
                -1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(AssertionError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, -1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(AssertionError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                -1 * apu.km, 1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(AssertionError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, -1 * apu.km, 30 * apu.deg
                )

        with pytest.raises(AssertionError):
            atm.slant_attenuation_annex2(
                1 * cnv.dB / apu.km, 1 * cnv.dB / apu.km,
                1 * apu.km, 1 * apu.km, 130 * apu.deg
                )

        atten_dry = Quantity([
                0.006643591, 0.008556794, 0.0200009175, 6.5824558517,
                0.0215553521
                ], cnv.dB / apu.km)

        atten_wet = Quantity([
                0.0082768112, 0.0599180804, 0.096043373, 0.1902800424,
                0.5888230557
                ], cnv.dB / apu.km)

        atten_tot = atm.slant_attenuation_annex2(
            atten_dry, atten_wet,
            10 * apu.km, 1 * apu.km, 30 * apu.deg
            )

        assert_quantity_allclose(
            atten_tot,
            Quantity([
                0.1494254424, 0.2909720408, 0.592105096,
                132.0296771188, 1.6087531534
                ], cnv.dB)
            )
