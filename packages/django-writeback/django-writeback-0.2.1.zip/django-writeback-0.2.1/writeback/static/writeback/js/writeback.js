(function ($) {

    $.fn.writeBack = function () {

        this.appendTo('body');

        var writeBack = {

            element: this,

            form: this.find('form'),

            init: function () {

                writeBack.showModalWindow();
                writeBack.closeModalWindow();
                writeBack.preventDataLoss();
                writeBack.ajaxFormSubmit();

            },


            showModalWindow: function () {

                $('#writeback_button').click(function (e) {
                    e.preventDefault();
                    $('.error_msg').remove();
                    writeBack.element.removeClass().addClass('show_window');
                });

            },


            closeModalWindow: function () {
                // Bind close-link clicked, outside the modal window click, Esc-key pressed.

                var removeShowWindowClass = function () {
                    writeBack.element.removeClass('show_window');
                };

                writeBack.element.find('.close').click(function (e) {
                    e.preventDefault();
                    removeShowWindowClass();
                });

                writeBack.element.click(function (e) {
                    var container = $(this).find('.window');
                    if (!container.is(e.target) // if the target of the click isn't the container...
                        && container.has(e.target).length === 0) // ... nor a descendant of the container
                    {
                        removeShowWindowClass();
                    }
                });

                $(document).keyup(function (e) {
                    if (e.keyCode == 27) {
                        removeShowWindowClass();
                    }
                });

            },


            preventDataLoss: function () {
                // Suggest staying on the page, if the form changed.

                if (writeBack.form.length > 0) {
                    var original = writeBack.form.serialize();
                    writeBack.form.submit(function () {
                        window.onbeforeunload = null
                    });
                    window.onbeforeunload = function () {
                        if (writeBack.form.serialize() != original && writeBack.element.is('[class=show_window]'))
                            return 'Are you sure, you want to leave this page? All unsaved data will be lost!'
                    }
                }

            },


            ajaxFormSubmit: function () {
                // Send the form through AJAX.

                writeBack.form.submit(function(e){
                    e.preventDefault();
                    var theform = $(this);

                    $.ajax({
                        data: theform.serialize(),
                        type: 'POST',
                        url: theform.attr('action'),
                        success: function() {
                            writeBack.element.removeClass('show_loader show_error').addClass('show_thankyou');
                        },
                        error: function(xhr) {
                            writeBack.element.removeClass('show_loader show_thankyou').addClass('show_error');
                            $('.error_msg').remove();
                            var obj = $.parseJSON(xhr.responseText);
                            $.each(obj, function(index, value) {
                                if (index=='__all__'){
                                    theform.find('.loader').before('<p class="error_msg">' + value + '</p>');
                                } else {
                                    $('#id_'+index).parent().before('<p class="error_msg">' + value + '</p>');
                                }

                            });
                        }
                    });
                    return false;
                });

            }


        };


        writeBack.init();

        return this;


    };

}(jQuery));
