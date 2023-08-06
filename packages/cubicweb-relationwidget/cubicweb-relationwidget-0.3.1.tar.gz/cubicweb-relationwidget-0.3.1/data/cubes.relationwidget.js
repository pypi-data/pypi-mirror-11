/* jshint strict: false, white: true */
/* global cw: false, Namespace: false, _: false */

cw.cubes.relationwidget = new Namespace('cw.cubes.relationwidget');

(function ($) {
    $.fn.relationwidget = function (options) {
        var $widget = $(this),
            widgetuid = $widget.attr('id'),
            defaultSettings = {
                editOptions: {
                    required: false,
                    multiple: true,
                    searchurl: '<required-option>'
                },
                dialogOptions: {
                    modal: true,
                    width: 600,
                    height: 800,
                    buttons: [
                        {
                            id: 'button-validate',
                            text: _('button_ok'),
                            click: function () {
                                validate($(this));
                            }
                        },
                        {
                            id: 'button-cancel',
                            text: _('cancel'),
                            click: function () {
                                $(this).dialog('close');
                            }
                        }
                    ],
                    close: function () {
                        $widget.empty();
                        // unbind $widget
                        $widget.off('server-response');
                        $widget.off('click');
                        $(this).dialog('destroy');
                    }
                }
            };
        if (options.onValidate) { onValidate = options.onValidate;}
        else {
            function onValidate(selected) {
                var $divgroup = $('#inputs-for-' + widgetuid);
                $divgroup.empty();
                var snippets = widgetuid.split('-');
                var inputname = snippets[1] + '-' + snippets[2] + ':' + snippets[3];
                for (var eid in selected) {
                    var label = selected[eid];
                    $divgroup.append(
                        $('<div class="checkbox"/>').append(
                            $('<label/>').html(' ' + label).prepend(
                                $('<input/>').attr({
                                    type: 'checkbox', checked: 'checked',
                                    name: inputname, value: eid,
                                    id: (inputname + '-' + eid),
                                    'data-html-label': label}
                                                  )
                            )
                        )
                    );
                }
            }
        }
        var editSettings = $.extend({}, defaultSettings.editOptions, options.editOptions),
            dialogSettings = $.extend({}, defaultSettings.dialogOptions, options.dialogOptions);

        function validate($modalDialog) {
            var $alert = $('#cw-relationwidget-alert');
            $alert.empty().addClass('hidden');
            var selected = getSelectedValues();
            if (editSettings.required && Object.keys(selected).length === 0) {
                $alert.text(_('required_error')).removeClass('hidden');
                return;
            }
            onValidate(selected);
            $modalDialog.dialog('close');
        }

        function initSelected() {
            // open entities link in new tab
            $('#cw-relationwidget-table table a').attr('target', '_blank');
            var $selected = $('#inputs-for-' + widgetuid + ' input');
            if ($selected.length === 0) {
                var label = $('<div/>').text(_('no selected entities'));
                $('#cw-relationwidget-linked-summary').append(label);
            } else {
                $selected.each(function (index, input) {
                    var $input = $(input);
                    if ($input.prop("checked")) {
                        var eid = $input.attr('value');
                        addOrUpdateCheckbox(eid, $input.data('html-label'), true);
                        $('#cw-relationwidget-table input[value='+eid+']').prop("checked", true);
                    }
                });
            }
        }

        function getSelectedValues() {
            var selected = {};
            $('#cw-relationwidget-linked-summary label').each(function () {
                var $this = $(this);
                var eid = $this.find('input:checked').attr('id');
                if (eid) {
                    selected[eid] = $('a', $this)[0].outerHTML;
                }
            });
            return selected;
        }

        function syncCheckboxes() {
            // syncCheckboxes MUST be called after each pagination on 'server-response'
            // which allows to know when to refresh this for the prev/next pages,
            // open entities link in new tab
            $('#cw-relationwidget-table table a').attr('target', '_blank');
            var selected = getSelectedValues();
            for (var eid in selected) {
                var $input = $('#cw-relationwidget-table input[value='+eid+']');
                if ($input.length === 1) {
                    // this input can be on another page
                    $input.prop('checked', 'checked');}
            }
        }

        function emptyData() {
            $('#cw-relationwidget-linked-summary').empty();
            var label = $('<div/>').text(_('no selected entities'));
            $('#cw-relationwidget-linked-summary').append(label);
        }

        function toggleRelatedCheckbox(eid, check) {
            var $input = $('#cw-relationwidget-table input[value='+eid+']');
            $input.prop("checked", check);
        }

        function addOrUpdateCheckbox(eid, htmlLabel, checked) {
            $('#cw-relationwidget-linked-summary div').hide();
            var $input = $('input#' + eid);
            if ($input.length === 0) {
                if (checked) {
                    $('#cw-relationwidget-linked-summary').append(
                        $('<li/>').addClass('add_related').append(
                            $('<label/>').html(' ' + htmlLabel).prepend(
                                $('<input type="checkbox" checked="checked">')
                                    .attr('id', eid)
                                    .click(function () {
                                        toggleRelatedCheckbox(eid, $(this).prop('checked'));
                                    })
                            )
                        )
                    );
                }
            }
            else {
                $input.prop("checked", checked);
            }
        }

        // instantiate the dialog window
        $widget.dialog(dialogSettings);
        var d = $widget.loadxhtml(editSettings.searchurl);
        d.addCallback(function () {
            // bind the pagination response to synchronize the checked values
            // fixme should only do this on the pagination callback, but
            // this is not possible for the moment
            $widget.bind('server-response', function (e) {syncCheckboxes();});
            var checkboxesSelector = '#cw-relationwidget-table input[type=checkbox]';
            $widget.on('click', checkboxesSelector, function (e) {
                var $input = $(this);
                // uncheck other selected inputs
                $('#cw-relationwidget-table input[type=checkbox]:not([value=' + $input.attr('value') + '])').prop('checked', false);
                var htmlLabel = $input.closest('tr').find('td[data-label-cell]').html();
                var checked = $input.prop('checked');
                if (!editSettings.multiple && checked) {
                    // only one value can be set on this relation
                    emptyData();
                }
                addOrUpdateCheckbox(this.value, htmlLabel, checked);
            });
            initSelected();
        });
    };
})(jQuery);
