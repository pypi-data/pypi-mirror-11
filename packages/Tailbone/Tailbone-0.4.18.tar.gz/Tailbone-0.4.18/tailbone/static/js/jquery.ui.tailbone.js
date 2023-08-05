// -*- coding: utf-8 -*-
/**********************************************************************
 * jQuery UI plugins for Tailbone
 **********************************************************************/

/**********************************************************************
 * gridwrapper plugin
 **********************************************************************/

(function($) {
    
    $.widget('tailbone.gridwrapper', {

        _create: function() {

            var that = this;

            // Snag some element references.
            this.filters = this.element.find('.newfilters');
            this.add_filter = this.filters.find('#add-filter');
            this.apply_filters = this.filters.find('#apply-filters');
            this.grid = this.element.find('.newgrid');

            // Enhance filters etc.
            this.filters.find('.filter').gridfilter();
            this.apply_filters.button('option', 'icons', {primary: 'ui-icon-search'});
            if (! this.filters.find('.active:checked').length) {
                this.apply_filters.button('disable');
            }
            this.add_filter.selectmenu({
                width: '15em',

                // Initially disabled if contains no enabled filter options.
                disabled: this.add_filter.find('option:enabled').length == 1,

                // When add-filter choice is made, show/focus new filter value input,
                // and maybe hide the add-filter selection or show the apply button.
                change: function (event, ui) {
                    var filter = that.filters.find('#filter-' + ui.item.value);
                    var select = $(this);
                    var option = ui.item.element;
                    filter.gridfilter('active', true);
                    filter.gridfilter('focus');
                    select.val('');
                    option.attr('disabled', 'disabled');
                    select.selectmenu('refresh');
                    if (select.find('option:enabled').length == 1) { // prompt is always enabled
                        select.selectmenu('disable');
                    }
                    that.apply_filters.button('enable');
                }
            });

            // Intercept filters form submittal, and submit via AJAX instead.
            this.filters.find('form').on('submit', function() {
                var form = $(this);

                var settings = {filter: true, partial: true};
                form.find('.filter').each(function() {

                    // currently active filters will be included in form data
                    if ($(this).gridfilter('active')) {
                        settings[$(this).data('key')] = $(this).gridfilter('value');
                        settings[$(this).data('key') + '.verb'] = $(this).gridfilter('verb');

                    // others will be hidden from view
                    } else {
                        $(this).gridfilter('hide');
                    }
                });

                // if no filters are visible, disable submit button
                if (! form.find('.filter:visible').length) {
                    that.apply_filters.button('disable');
                }

                // okay, submit filters to server and refresh grid
                that.refresh(settings);
                return false;
            });

            // Refresh data when user clicks a sortable column header.
            this.element.on('click', 'thead th.sortable a', function() {
                var th = $(this).parent();
                var data = {
                    sortkey: th.data('sortkey'),
                    sortdir: (th.hasClass('sorted') && th.hasClass('asc')) ? 'desc' : 'asc',
                    page: 1,
                    partial: true
                };
                that.refresh(data);
                return false;
            });

            // Refresh data when user chooses a new page size setting.
            this.element.on('change', '.pager #pagesize', function() {
                var settings = {
                    partial: true,
                    pagesize: $(this).val()
                };
                that.refresh(settings);
            });

            // Refresh data when user clicks a pager link.
            this.element.on('click', '.pager a', function() {
                that.refresh(this.search.substring(1)); // remove leading '?'
                return false;
            });

            // Add hover highlight effect to grid rows during mouse-over.
            this.element.on('mouseenter', 'tbody tr', function() {
                $(this).addClass('hovering');
            });
            this.element.on('mouseleave', 'tbody tr', function() {
                $(this).removeClass('hovering');
            });

            // Show 'more' actions when user hovers over 'more' link.
            this.element.on('mouseenter', '.actions a.more', function() {
                that.grid.find('.actions div.more').hide();
                $(this).siblings('div.more')
                    .show()
                    .position({my: 'left-5 top-4', at: 'left top', of: $(this)});
            });
            this.element.on('mouseleave', '.actions div.more', function() {
                $(this).hide();
            });
        },

        // Refreshes the visible data within the grid, according to the given settings.
        refresh: function(settings) {
            var that = this;
            this.element.mask("Refreshing data...");
            $.get(this.grid.data('url'), settings, function(data) {
                that.grid.replaceWith(data);
                that.grid = that.element.find('.newgrid');
                that.element.unmask();
            });
        }

    });
    
})( jQuery );


/**********************************************************************
 * gridfilter plugin
 **********************************************************************/

(function($) {
    
    $.widget('tailbone.gridfilter', {

        _create: function() {

            // Track down some important elements.
            this.checkbox = this.element.find('input[name$="-active"]');
            this.label = this.element.find('label');
            this.inputs = this.element.find('.inputs');
            this.add_filter = this.element.parents('.newgrid-wrapper').find('#add-filter');

            // Hide the checkbox and label, and add button for toggling active status.
            this.checkbox.addClass('ui-helper-hidden-accessible');
            this.label.hide();
            this.activebutton = $('<button type="button" class="toggle" />')
                .insertAfter(this.label)
                .text(this.label.text())
                .button({
                    icons: {primary: 'ui-icon-blank'}
                });

            // Enhance some more stuff.
            this.inputs.find('.verb').selectmenu({width: '15em'});

            // Listen for button click, to keep checkbox in sync.
            this._on(this.activebutton, {
                click: function(e) {
                    var checked = !this.checkbox.is(':checked');
                    this.checkbox.prop('checked', checked);
                    this.refresh();
                    if (checked) {
                        this.focus();
                    }
                }
            });

            // Update the initial state of the button according to checkbox.
            this.refresh();
        },

        refresh: function() {
            if (this.checkbox.is(':checked')) {
                this.activebutton.button('option', 'icons', {primary: 'ui-icon-check'});
                this.inputs.show();
            } else {
                this.activebutton.button('option', 'icons', {primary: 'ui-icon-blank'});
                this.inputs.hide();
            }
        },

        active: function(value) {
            if (value === undefined) {
                return this.checkbox.is(':checked');
            }
            if (value) {
                if (!this.checkbox.is(':checked')) {
                    this.checkbox.prop('checked', true);
                    this.refresh();
                    this.element.show();
                }
            } else if (this.checkbox.is(':checked')) {
                this.checkbox.prop('checked', false);
                this.refresh();
            }
        },

        hide: function() {
            this.active(false);
            this.element.hide();
            var option = this.add_filter.find('option[value="' + this.element.data('key') + '"]');
            option.attr('disabled', false);
            if (this.add_filter.selectmenu('option', 'disabled')) {
                this.add_filter.selectmenu('enable');
            }
            this.add_filter.selectmenu('refresh');
        },

        focus: function() {
            this.inputs.find('.value input').focus();
        },

        value: function() {
            return this.inputs.find('.value input').val();
        },

        verb: function() {
            return this.inputs.find('.verb').val();
        }

    });
    
})( jQuery );
