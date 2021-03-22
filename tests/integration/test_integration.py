"""Integration tests."""

import subprocess


def test_installation():
    """Build and run docker container."""
    subprocess.run(
        ["docker", "build", "-t", "misosoup_test_container", "."], check=False
    )
    complete_process = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            "misosoup_test_container_run",
            "misosoup_test_container",
            "misosoup",
            "-h",
        ],
        check=False,
    )
    assert complete_process.returncode == 0


def test_integration():
    """Run docker container on data."""
    complete_process = subprocess.run(
        [
            "misosoup",
            "--base-medium",
            "tests/data/medium.yaml",
            "--carbon-sources",
            "ac",
            "--strain",
            "A1R12",
            "--parsimony",
            "tests/data/A1R12.xml",
            "tests/data/I2R16.xml",
        ],
        capture_output=True,
        check=False,
    )
    assert complete_process.returncode == 0
    assert (
        complete_process.stdout
        == b"""Academic license - for non-commercial use only - expires 2021-05-13
Using license file /Users/TheUser/.config/gurobi/gurobi.lic
ac:
  A1R12:
  - Growth_A1R12: 0.009999999998544616
    Growth_I2R16: 0.16532951282622593
    R_EX_2ohph_c: 5.480170534242842e-17
    R_EX_3hcinnm_e: 4.361183907377901e-19
    R_EX_3hcinnm_e_I2R16_INT: 5.184866642486556e-16
    R_EX_4abut_e: 1.8851531729824857e-14
    R_EX_4abut_e_A1R12_INT: 1.8851531729824854e-14
    R_EX_4crsol_c: 5.109640349263562e-16
    R_EX_4hba_c: 3.570413778650548e-05
    R_EX_4hphac_e: 1.7924791948977732e-19
    R_EX_4hphac_e_I2R16_INT: 1.878244982565489e-14
    R_EX_5drib_c: 1.9368379991164045e-06
    R_EX_5mtr_e: 2.0945976450785993e-16
    R_EX_5mtr_e_I2R16_INT: 2.0945976450785998e-16
    R_EX_LalaDgluMdapDala_e: 3.9110265939376746e-14
    R_EX_LalaDgluMdapDala_e_A1R12_INT: 3.911026593937674e-14
    R_EX_LalaDgluMdap_e: 5.048873145549341e-14
    R_EX_LalaDgluMdap_e_A1R12_INT: 5.048873145549341e-14
    R_EX_ac_e: -9.994409487617153
    R_EX_ac_e_A1R12_INT: 0.7729250328976605
    R_EX_ac_e_I2R16_INT: -10.76733452051451
    R_EX_acald_e: 4.798761492497339e-16
    R_EX_acald_e_A1R12_INT: -1.1209810930675985
    R_EX_acald_e_I2R16_INT: 1.1209810930677122
    R_EX_ade_e: 3.9398113955638805e-14
    R_EX_ade_e_I2R16_INT: 3.9398113955638805e-14
    R_EX_ala__D_e: 3.360595187362893e-16
    R_EX_ala__D_e_A1R12_INT: 0.7602869702972157
    R_EX_ala__D_e_I2R16_INT: -0.760286970297102
    R_EX_ala__L_e: 3.3599552684926845e-16
    R_EX_ala__L_e_A1R12_INT: 1.2168012256689735
    R_EX_ala__L_e_I2R16_INT: -1.2168012256687462
    R_EX_anhgm_e: 2.7971477811417016e-16
    R_EX_anhgm_e_A1R12_INT: 2.797147781141701e-16
    R_EX_arab__L_e: 8.676010387614369e-19
    R_EX_arab__L_e_I2R16_INT: 8.676010387614369e-19
    R_EX_asp__L_e: 3.4086253524335217e-16
    R_EX_asp__L_e_A1R12_INT: -0.582663731899288
    R_EX_asp__L_e_I2R16_INT: 0.5826637318995154
    R_EX_bmocogdp_c: 3.62738882051285e-14
    R_EX_bz_e: 1.4031517149294292e-14
    R_EX_bz_e_I2R16_INT: 1.403151714929429e-14
    R_EX_ca2_e: -0.0008837696043428878
    R_EX_ca2_e_A1R12_INT: -5.040620885665703e-05
    R_EX_ca2_e_I2R16_INT: -0.0008333633954282771
    R_EX_cgly_e: 5.296366758235761e-19
    R_EX_cgly_e_I2R16_INT: 1.3576723505304186e-14
    R_EX_chol_e: 4.856988558108888e-19
    R_EX_cl_e: -0.0008837696042813814
    R_EX_cl_e_A1R12_INT: -5.0406208853048806e-05
    R_EX_cl_e_I2R16_INT: -0.0008333633954282771
    R_EX_co2_e: 12.744494388610127
    R_EX_co2_e_A1R12_INT: 0.618392717993288
    R_EX_co2_e_I2R16_INT: 12.126101670617004
    R_EX_cobalt2_e: -1.6979243014247913e-05
    R_EX_cobalt2_e_A1R12_INT: -9.684190445113927e-07
    R_EX_cobalt2_e_I2R16_INT: -1.601082396973652e-05
    R_EX_cu2_e: -0.00012038283364290692
    R_EX_cu2_e_A1R12_INT: -6.866090643598e-06
    R_EX_cu2_e_I2R16_INT: -0.00011351674299930892
    R_EX_drib_e: 4.0243694553219377e-19
    R_EX_drib_e_A1R12_INT: 3.221162217363563e-14
    R_EX_enlipa_e: 1.5022927281052744e-16
    R_EX_enlipa_e_A1R12_INT: 6.116891943656056e-17
    R_EX_enlipa_e_I2R16_INT: 8.906035337396699e-17
    R_EX_etha_e: 1.8743476299304294e-15
    R_EX_etha_e_A1R12_INT: 1.8743476299304286e-15
    R_EX_etoh_e: 4.092237888112508e-16
    R_EX_etoh_e_A1R12_INT: -0.18471900859094603
    R_EX_etoh_e_I2R16_INT: 0.18471900859105972
    R_EX_fe2_e: -0.002465895477939739
    R_EX_fe2_e_A1R12_INT: -0.0013907686384300177
    R_EX_fe2_e_I2R16_INT: -0.0010751268396234082
    R_EX_fe3_e: 1.1616700884941795e-14
    R_EX_fe3_e_A1R12_INT: 0.0012501251473224847
    R_EX_fe3_e_I2R16_INT: -0.0012501251472940567
    R_EX_fol_e: -6.478723662439734e-06
    R_EX_fol_e_A1R12_INT: -6.478723662439734e-06
    R_EX_fuc__L_e: 1.1999435344603868e-18
    R_EX_fuc__L_e_I2R16_INT: 1.1999435344603864e-18
    R_EX_g3pe_e: 2.087678426996245e-14
    R_EX_g3pe_e_A1R12_INT: 2.087678426996245e-14
    R_EX_g3pg_e: 1.9786851025738e-14
    R_EX_g3pg_e_A1R12_INT: 1.9786851025738e-14
    R_EX_galur_e: 8.963098999038525e-19
    R_EX_galur_e_I2R16_INT: 8.963098999038523e-19
    R_EX_glcur_e: 9.215885229078137e-19
    R_EX_glcur_e_I2R16_INT: 9.215885229078137e-19
    R_EX_glu__L_e: 2.3278256934617674e-16
    R_EX_glu__L_e_A1R12_INT: 0.5068088792165781
    R_EX_glu__L_e_I2R16_INT: -0.5068088792164644
    R_EX_gly_e: 5.992613362270205e-16
    R_EX_gly_e_A1R12_INT: -0.0215874249273611
    R_EX_gly_e_I2R16_INT: 0.021587424927474785
    R_EX_glyb_e: 3.3582464258381124e-18
    R_EX_glyb_e_I2R16_INT: 1.7043148389371618e-18
    R_EX_glyc_e: 3.04139839094905e-16
    R_EX_glyc_e_A1R12_INT: 9.68418476077204e-07
    R_EX_glyc_e_I2R16_INT: -9.684183623903664e-07
    R_EX_gm1lipa_e: 2.2452453654535235e-16
    R_EX_gm1lipa_e_A1R12_INT: 8.857232731282343e-17
    R_EX_gm1lipa_e_I2R16_INT: 1.3595220923252903e-16
    R_EX_gthox_e: 2.2327783637456276e-19
    R_EX_gthox_e_A1R12_INT: 1.4526873735542836
    R_EX_gthox_e_I2R16_INT: -1.4526873735542836
    R_EX_gthrd_e: 4.942569364240889e-19
    R_EX_gthrd_e_A1R12_INT: -2.905374747108567
    R_EX_gthrd_e_I2R16_INT: 2.905374747108567
    R_EX_h2_e: 2.9473064396271474e-14
    R_EX_h2_e_A1R12_INT: 2.947306439627147e-14
    R_EX_h2o2_e: 2.314564666999584e-18
    R_EX_h2o2_e_A1R12_INT: -1.4526873735542836
    R_EX_h2o2_e_I2R16_INT: 1.4526873735542836
    R_EX_h2o_e: 17.72409395648299
    R_EX_h2o_e_A1R12_INT: 3.777641170780271
    R_EX_h2o_e_I2R16_INT: 13.946452785702604
    R_EX_h2s_e: 2.485719535763615e-16
    R_EX_h2s_e_A1R12_INT: -0.0023829402082355955
    R_EX_h2s_e_I2R16_INT: 0.002382940208462969
    R_EX_h_e: -8.726133245748542
    R_EX_h_e_A1R12_INT: 0.6406175122359627
    R_EX_h_e_I2R16_INT: -9.366750757984391
    R_EX_hemeO_c: 6.169652162670953e-17
    R_EX_ile__L_e: 1.260008930418936e-16
    R_EX_ile__L_e_A1R12_INT: 2.8019190320776038e-14
    R_EX_inost_e: 9.452410067979209e-16
    R_EX_inost_e_A1R12_INT: 2.778967983546191e-16
    R_EX_k_e: -0.033142294018944085
    R_EX_k_e_A1R12_INT: -0.0018902860949765454
    R_EX_k_e_I2R16_INT: -0.031252007923740166
    R_EX_kdo2lipid4_e: 7.637098696561832e-17
    R_EX_kdo2lipid4_e_A1R12_INT: 3.0179825747633505e-17
    R_EX_kdo2lipid4_e_I2R16_INT: 4.619116121798482e-17
    R_EX_lac__D_e: 1.7907599237821118e-14
    R_EX_lac__D_e_A1R12_INT: 1.7907599237821118e-14
    R_EX_lac__L_e: 3.7591686887104185e-14
    R_EX_lac__L_e_I2R16_INT: 3.759168688710419e-14
    R_EX_leu__L_e: 1.432276941656514e-16
    R_EX_leu__L_e_A1R12_INT: 4.9565943278864326e-14
    R_EX_leu__L_e_I2R16_INT: -5.684341886080802e-14
    R_EX_lipa_cold_e: 8.438916968471943e-17
    R_EX_lipa_cold_e_A1R12_INT: 3.461223686535195e-17
    R_EX_lipa_cold_e_I2R16_INT: 4.9776932819367505e-17
    R_EX_lipa_e: 4.688962347930581e-17
    R_EX_lipa_e_A1R12_INT: 1.8664885012680994e-17
    R_EX_lipa_e_I2R16_INT: 2.822473846662481e-17
    R_EX_lipopb_c: 3.176718424866984e-16
    R_EX_lys__L_e: 1.1756350911490185e-16
    R_EX_mg2_e: -0.001472949340469043
    R_EX_mg2_e_A1R12_INT: -8.401034808813712e-05
    R_EX_mg2_e_I2R16_INT: -0.001388938992381128
    R_EX_mn2_e: -0.00011732657003449276
    R_EX_mn2_e_A1R12_INT: -6.691775297440472e-06
    R_EX_mn2_e_I2R16_INT: -0.00011063479450967861
    R_EX_mobd_e: 1.1368683772161603e-13
    R_EX_mobd_e_I2R16_INT: -5.684341886080802e-14
    R_EX_mththf_c: 5.073029145678021e-16
    R_EX_nh4_e: -1.9011475666587785
    R_EX_nh4_e_A1R12_INT: -1.9880258041989691
    R_EX_nh4_e_I2R16_INT: 0.08687823754041801
    R_EX_o2_e: -12.519876111139183
    R_EX_o2_e_A1R12_INT: -0.006243124389357035
    R_EX_o2_e_I2R16_INT: -12.513632986749712
    R_EX_pdima_e: 1.114614886491086e-16
    R_EX_pdima_e_A1R12_INT: 1.114614886491086e-16
    R_EX_pheme_e: 3.5299374379579797e-16
    R_EX_pheme_e_A1R12_INT: 1.7147348503467255e-16
    R_EX_pheme_e_I2R16_INT: 1.8152025876112537e-16
    R_EX_pi_e: -0.1674311278359255
    R_EX_pi_e_A1R12_INT: -0.009549511941031597
    R_EX_pi_e_I2R16_INT: -0.1578816158950076
    R_EX_pro__L_e: 1.7037375368515116e-16
    R_EX_pro__L_e_I2R16_INT: 2.034853318510533e-14
    R_EX_pydxn_e: -2.1595743654560795e-06
    R_EX_pydxn_e_A1R12_INT: -2.1595743654560795e-06
    R_EX_pyr_e: 4.061300288969424e-16
    R_EX_pyr_e_A1R12_INT: -2.0191153918593727
    R_EX_pyr_e_I2R16_INT: 2.0191153918593727
    R_EX_rib__D_e: 2.042910920523597e-15
    R_EX_s_e: 9.031011678676695e-14
    R_EX_s_e_A1R12_INT: 3.4126331345414433e-15
    R_EX_s_e_I2R16_INT: 8.689748365222537e-14
    R_EX_ser__D_e: 2.3576579847649924e-14
    R_EX_ser__D_e_I2R16_INT: 2.357657984764993e-14
    R_EX_sheme_c: 1.9083124941891096e-16
    R_EX_so4_e: -0.04255223828056387
    R_EX_so4_e_A1R12_INT: -4.201001604542398e-05
    R_EX_so4_e_I2R16_INT: -0.04251022826440476
    R_EX_spmd_e: 6.997025336672004e-16
    R_EX_spmd_e_A1R12_INT: 4.658141660898047e-16
    R_EX_spmd_e_I2R16_INT: 2.3388836757739553e-16
    R_EX_thm_e: -2.1595743656885324e-06
    R_EX_thm_e_A1R12_INT: -2.1595743656885324e-06
    R_EX_udcpo5_e: 2.755921093580358e-14
    R_EX_udcpo5_e_A1R12_INT: 2.7559210935803577e-14
    R_EX_val__L_e: 1.72994578780163e-16
    R_EX_val__L_e_A1R12_INT: 4.623078354678747e-14
    R_EX_zn2_e: -5.789921920040797e-05
    R_EX_zn2_e_A1R12_INT: -3.3023087553374353e-06
    R_EX_zn2_e_I2R16_INT: -5.45969103313837e-05
    community_growth: 0.17532951282477055
    y_I2R16: 1.0

"""
    )
