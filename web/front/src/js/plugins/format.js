const formatPercentage = (value) => (value * 100).toFixed(2) + '%';
const formatCurrency = (value, currency="") => value.toFixed(2) + " " + currency;
const formatFloat = (value) => value.toFixed(2);

export {formatCurrency, formatPercentage, formatFloat};
