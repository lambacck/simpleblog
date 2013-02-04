/* Project specific Javascript goes here. */
(function($) {
    var new_comment_form = null;
    var new_comment_container = null;
    var validator = null;
    var slug_changed = false;
    var slug_el = null;
    var title_el = null;

    var post_comment = function(form) {
        var self = $(form);
        var data = 'format=json&' + self.serialize();
        var options = {
            data: data,
            dataType: 'json',
            type: 'POST'
        };

        $.ajax(form.action, options)
            .then(
                function(result) {
                    var messages;

                    if (!result.success) {
                        validator.showErrors(result.errors);
                        return;
                    }

                    if (!new_comment_container) {
                        new_comment_container = $('#new-comment');
                    }

                    self.siblings('.messages').hide('slow', function() { $(this).remove(); });

                    $('<ul class="messages"></ul>').append($().add($.map(result.messages, function(val) {
                        return $('<li>').text(val.message).prop('className', val.tags)[0];
                    }))).insertBefore(self);

                    $(result.comment).insertBefore(new_comment_container).hide().show('slow');
                    $('#id_body')[0].value = '';
                },
                function(error) {
                    if (console) {
                        console.log(error);
                    }
                }
            );

        return false;
    };

    $(function() {
        new_comment_form = $('#new-comment-form');
        if (new_comment_form.length) {
            // comment form ui
            validator = new_comment_form.validate({
                submitHandler: post_comment
            });
        }

        var pub_date = $('#id_pub_date');
        var first_stage_re = /[^\-\w\s]/g;
        var second_stage_re = /[\-\s]+/g;
        if (pub_date.length) {
            // post form ui
            pub_date.datepicker({dateFormat: 'yy-mm-dd'});
            slug_el = $('#id_slug').keyup(function() {
                slug_changed = true;
            });
            if (slug_el[0].value) {
                slug_changed = true;
            }
            title_el = $('#id_title').keyup(function() {
                if (slug_changed) {
                    return;
                }

                var value = this.value;
                value = $.trim(value.replace(first_stage_re, '')).toLowerCase();
                value = value.replace(second_stage_re, '-');

                slug_el[0].value = value;
            });
        }
    });
})(jQuery);
