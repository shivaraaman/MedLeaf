(function($) {
    // Check for HTML5 multiple file support
    var multipleSupport = typeof $('<input/>')[0].multiple !== 'undefined',
        isIE = /msie/i.test(navigator.userAgent);

    $.fn.customFile = function() {
        return this.each(function() {
            var $file = $(this).addClass('custom-file-upload-hidden'),
                $wrap = $('<div class="file-upload-wrapper">'),
                $input = $('<input type="text" class="file-upload-input" />'),
                $button = $('<button type="button" class="file-upload-button">Select a File</button>'),
                $label = $('<label class="file-upload-button" for="' + $file[0].id + '">Select a File</label>');

            $file.css({ position: 'absolute', left: '-9999px' });
            $wrap.insertAfter($file).append($file, $input, (isIE ? $label : $button));

            $file.attr('tabIndex', -1);
            $button.attr('tabIndex', -1).click(function() { $file.focus().click(); });

            $file.change(function() {
                var filename = multipleSupport ? $file[0].files.map(function(file) { return file.name; }).join(', ') : $file.val().split('\\').pop();
                $input.val(filename).attr('title', filename).focus();
            });

            $input.on({
                blur: function() { $file.trigger('blur'); },
                keydown: function(e) {
                    if (e.which === 13) { !isIE && $file.trigger('click'); }
                    else if (e.which === 8 || e.which === 46) { $file.replaceWith($file = $file.clone(true)).trigger('change'); $input.val(''); }
                    else if (e.which === 9) { return; }
                    else { return false; }
                }
            });
        });
    };

    // Old browser fallback
    if (!multipleSupport) {
        $(document).on('change', 'input.customfile', function() {
            var $this = $(this), uniqId = 'customfile_' + (new Date()).getTime(), $wrap = $this.parent(), $inputs = $wrap.siblings().find('.file-upload-input').filter(function() { return !this.value }), $file = $('<input type="file" id="' + uniqId + '" name="' + $this.attr('name') + '"/>');

            setTimeout(function() {
                if ($this.val()) {
                    if (!$inputs.length) {
                        $wrap.after($file);
                        $file.customFile();
                    }
                } else {
                    $inputs.parent().remove();
                    $wrap.appendTo($wrap.parent());
                    $wrap.find('input').focus();
                }
            }, 1);
        });
    }
})(jQuery);

$('input[type=file]').customFile();
$(document).ready(function() {
    $('#uploadButton').on('click', function() {
        var formData = new FormData();
        var files = $('#fileInput')[0].files;

        // Add each selected file to the FormData object
        for (var i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }

        // Send the files to the server using AJAX
        $.ajax({
            url: '/upload', // Replace with your Python server endpoint
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Handle success response from the server
                console.log('Image uploaded successfully.');
            },
            error: function(xhr, status, error) {
                // Handle error response from the server
                console.error('Error uploading image:', error);
            }
        });
    });
});
