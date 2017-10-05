pre_mean, pre_variance, pre_max_val, pre_min_val, pre_rms, pre_velo, pre_sma, pre_ema, pre_energy = features_calc(data_vm[:pre_win],
data_x[:pre_win],data_y[:pre_win], data_z[:pre_win], freq_rate)

#impact_post
imp_mean, imp_variance, imp_max_val, imp_min_val, imp_rms, imp_velo, imp_sma, imp_ema, imp_energy = features_calc(data_vm[pre_win:imp],
data_x[pre_win:imp], data_y[pre_win:imp], data_z[pre_win:imp], freq_rate)

 #post impact
post_mean, post_variance, post_max_val, post_min_val, post_rms, post_velo, post_sma, post_ema, post_energy = features_calc(data_vm[imp:post_win],
data_x[imp:post_win], data_y[imp:post_win], data_z[imp:post_win], freq_rate)
