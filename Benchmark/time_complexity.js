const composer = require('openwhisk-composer')

module.exports = composer.sequence(
    composer.action('constant'),
    composer.action('logarithmic'),
    composer.action('linear'),
    composer.action('linearithmic'),
    composer.action('quadratic'),
    composer.action('cubic'))