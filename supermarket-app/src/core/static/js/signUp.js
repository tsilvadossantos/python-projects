$(function() {
    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
            	            	
                 //redirect route
                 if(data == '/'){
                 	alert('User created successfully!')
                 	window.location = data;
                 }else if (data == '/usercheck'){
                 	alert('Username already exists!');
                 }else if (data == '/checkField'){
                 	alert('Action Required: Input you details: name, username and password')
                 }
                 
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
