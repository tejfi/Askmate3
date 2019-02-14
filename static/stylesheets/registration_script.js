$('#exampleModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget) // Button that triggered the modal
  let recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  let modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
});







$('#exampleModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})



$('#modalRegistration').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget) // Button that triggered the modal
  let recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  let modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
});




$(document).ready(function() {
    $('#loginForm').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            user_name: {
                validators: {
                    notEmpty: {
                        message: 'The username is required'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'The password is required'
                    }
                }
            }
        }
    });
});
$(document).ready(function() {
    $('#loginForm').on('success.form.bv', function(e) {
        // Prevent form submission
        e.preventDefault();

        var validator = $(e.target).data('bootstrapValidator');
        $('#exampleModal')
            .one('hidden.bs.modal', function() {
                $('#exampleModal')
                    .find('.username')
                        .html(validator.getFieldElements('username').val()).end()
                    .modal('show');
            })
            .modal('hide');
    });

    $('#exampleModal').on('shown.bs.modal', function() {
        $('#loginForm').bootstrapValidator('resetForm', true)
                       .find('[name="username"]').focus();
    });
});



$(window).scroll(function(event) {
	function footer()
    {
        var scroll = $(window).scrollTop();
        if(scroll > 50)
        {
            $(".footer-nav").fadeIn("slow").addClass("show");
        }
        else
        {
            $(".footer-nav").fadeOut("slow").removeClass("show");
        }

        clearTimeout($.data(this, 'scrollTimer'));
        $.data(this, 'scrollTimer', setTimeout(function() {
            if ($('.footer-nav').is(':hover')) {
	        	footer();
    		}
            else
            {
            	$(".footer-nav").fadeOut("slow");
            }
		}, 2000));
    }
    footer();
});
