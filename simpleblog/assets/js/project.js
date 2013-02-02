/* Project specific Javascript goes here. */
(function($) {
    var new_comment_form = null;
    var new_comment_container = null;
    var validator = null;
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
                        self.showErrors(result.errors);
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
                    validator.resetForm();
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
        if (new_comment_form) {
            validator = new_comment_form.validate({
                submitHandler: post_comment
            });
        }
    });
})(jQuery);
