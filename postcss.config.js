const purgecss = require('@fullhuman/postcss-purgecss').default;

module.exports = {
  plugins: [
    purgecss({
      content: ['./templates/**/*.html'],
      safelist: [
        'show',
        'fade',
        'collapsing',
        'collapse',
        'active',
        'alert',
        'alert-success',
        'alert-danger',
        'alert-warning',
        'alert-info',
        'modal',
        'modal-open',
        'modal-dialog',
        'modal-backdrop',
        'dropdown-menu',
        'dropdown-item',
        'dropdown-toggle',
        'btn',
        'btn-primary',
        'btn-secondary',
        'btn-danger',
        'btn-success',
        'btn-warning',
        'btn-outline-primary',
        'btn-outline-secondary',
        'btn-outline-danger',
        'btn-outline-success',
        'btn-outline-warning',
        'disabled',
        'hidden',
        'd-block',
        'd-none'
      ],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
    })
  ]
};
