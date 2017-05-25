$(function() {
    $('#btnSignIn').click(function() {

        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                 //redirect route
                
                 if(data == '/'){
                 	 window.location = data;
                 }else if (data == '/usercheck'){
                 	alert('401 - Unauthorized: Check username and/or password');
                 }else if (data == '/checkField'){
                 	alert('Action Required: Input username and password')
                 }
                 
                              
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
