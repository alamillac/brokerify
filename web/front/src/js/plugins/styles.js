const color_threshold_style = (
    value,
    min_val,
    max_val,
    reverse = false,
    colors = ['red', 'green'],
) => {
    if (reverse) {
        colors = colors.slice(0);
        colors.reverse();
    }
    if (value < min_val) {
        return {color: colors[0]};
    }
    if (value > max_val) {
        return {color: colors[1]};
    }
    return {};
};

export {color_threshold_style};
