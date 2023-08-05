function displayPopup(event)
{
    /* Opens the target link into a dialog box
     *
     * The target link is extracted from the @href attribute for anchors or
     * from the @data-url attribute for other tags.
     *
     * The dialog title is extracted from "#appbar h2" (this selector can be
     * changed with a @data-title-selector attribute on the anchor tag).
     *
     * The dialog content is extracted from "form" (this selector can be
     * changed with a @data-selector attribute).
     *
     * Buttons (both <button> and <a>) are extracted from the content and
     * converted into proper dialog buttons.  A button with "cancel" as its
     * class will have its action changed to simply close the dialog, without
     * server processing.
     *
     * After loading the dialog content, a gadjo:dialog-loaded event is
     * triggered on the anchor with the dialog content as argument.
     *
     * Alternatively the server may notice the ajax request and answer with
     * an appropriate JSON response. In that case it should have a 'content'
     * attribute with the HTML content, or a 'location' attribute in case of
     * a redirect.
     *
     * In case of such a redirect, a gadjo:dialog-done event is triggered on
     * the anchor and can be cancelled to prevent the default redirect
     * behaviour.
     *
     * The JSON support depends on the presence of the jQuery Form plugin.
     */
    var $anchor = $(this);
    var url = $anchor.attr('href') || $anchor.data('url');
    var selector = $anchor.data('selector') || 'form:not(.gadjo-popup-ignore)';
    var title_selector = $anchor.data('title-selector') || '#appbar h2';

    function show_error(message) {
      /* Add a div to body to show an error message and fade it out after 3
       * seconds */
      $('<div id="gadjo-ajax-error"></div>')
        .text(message)
        .appendTo('body')
        .delay(3000)
        .fadeOut(400, function () {
          $(this).remove();
        });
    }

    function ajaxform_submit(data, status, xhr, form) {
        if ('location' in data) {
            var e = $.Event('gadjo:dialog-done');
            if (document.contains($anchor[0])) {
                $anchor.trigger(e, form);
            } else {
                $(document).trigger(e, form);
            }
            /* check if the event action has been prevented, and don't do
             * anything in that case. */
            if (! e.isDefaultPrevented()) {
                if (data.location.split('#')[0] == window.location.href.split('#')[0]) {
                    window.location.reload(true);
                }
                window.location = data.location;
            }
        } else {
            var $form = $(form);
            $form.empty().append($(data.content).find(selector).children());
            $form.find('.buttons').hide();
            if (document.contains($anchor[0])) {
              $anchor.trigger('gadjo:dialog-loaded', $form);
            } else {
              $(document).trigger('gadjo:dialog-loaded', $form);
            }
        }
    }

    /* Close existing dialog boxes */
    $(".ui-dialog-content").dialog("destroy");

    $.ajax({
        url: url,
        success: function(html) {
            var is_json = typeof html != 'string';
            if (is_json) {
                /* get html out of json */
                var html = html.content;
            } else {
                var html = html;
            }
            var $html = $(html);

            /* get content and form (if different) ouf of html */
            var $content = $html.find(selector);
            if ($content.is('form')) {
                var $form = $content;
            } else {
                var $form = $content.find('form');
            }

            /* get title out of html */
            var title = $html.find(title_selector).text();

            $form.dialog({
              modal: true, 
              'title': title,
              width: 'auto',
              close: function (ev, ui) { 
                $(this).dialog('destroy'); 
              },
            });

            /* if the form doesn't have an @action attribute, set it to URL */
            if (! $form.prop('action')) {
                $form.prop('action', url);
            }

            /* hide buttons from content and convert buttons (<button> and <a>)
             * into proper dialog buttons */
            $form.find('.buttons').hide();

            var buttons = Array();
            $form.find('.buttons button, .buttons a').each(function(idx, elem) {
                var $elem = $(elem);
                var button = Object();

                button.text = $elem.text();
                if ($elem.hasClass('cancel')) {
                    /* special behaviour for the cancel button: do not send
                     * anything to server, just close the dialog */
                    button.click = function() { $form.dialog('destroy'); return false; };
                } else {
                    button.click = function() { $form.find('button').click(); return false; };
                }

                /* add custom classes to some buttons */
                if ($elem.hasClass('submit-button')) {
                    button.class = 'submit-button';
                } else if ($elem.hasClass('delete-button')) {
                    button.class = 'delete-button';
                }
                buttons.push(button);
            });

            buttons.reverse();
            $form.dialog('option', 'buttons', buttons);

            /* focus initial input field */
            if ($form.find('input:visible').length) {
                $form.find('input:visible')[0].focus();
            }

            /* if received content was in json, apply jQuery Form plugin on it */
            if (is_json && $.fn.ajaxForm != undefined) {
                $form.ajaxForm({
                  success: ajaxform_submit,
                  error: function (jqXHR, textStatus, errorThrown) {
                    show_error("Dialog box submit failed: " + textStatus + " " + errorThrown);
                  }
                });
            }
            $anchor.trigger('gadjo:dialog-loaded', $form);
            return false;
        },
        error: function (jqXHR, textStatus, errorThrown) {
          show_error("Dialog box loading failed: " + textStatus + " " + errorThrown);
        }
    });
    return false;
}

$(function() {
  $(document).on('click.gadjo', 'a[rel=popup]', displayPopup);

  var sidepage_button = $('#sidepage #applabel');
  sidepage_button.on('click', function() {
    $('#sidepage, #main').addClass('enable-transitions');
    $('#sidepage, #main').toggleClass('sidepage-expanded');
    if ($('#sidepage').hasClass('sidepage-expanded')) {
       window.localStorage.sidepage_status = 'expanded';
    } else {
       window.localStorage.sidepage_status = null;
    }
  });
  if (window.location.protocol == 'file:') {
    /* don't open sidepage when loading from a file:// */
    window.localStorage.sidepage_status = null;
  }
  if (window.localStorage.sidepage_status === undefined &&
      typeof(GADJO_DEFAULT_SIDEPAGE_STATUS) !== "undefined") {
    window.localStorage.sidepage_status = GADJO_DEFAULT_SIDEPAGE_STATUS;
  }
  if (window.localStorage.sidepage_status == 'expanded') {
    $('#sidepage, #main').toggleClass('sidepage-expanded');
  }
});
