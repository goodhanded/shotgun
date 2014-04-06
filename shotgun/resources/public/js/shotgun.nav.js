$(document).ready(function(){
    $('#section-login').hide();
    $('#section-register').hide();
    var loginTime = 0;
    var signupTime = 0;
  
    $('#login').click(function(){
        $('#section-register').hide();
        signupTime=0;
        if(loginTime==0){
            $('#section-login').show();
            loginTime=1;
        }else{
            $('#section-login').hide();
            loginTime=0;
        }
    });

    $('#signup').click(function(){

        $('#section-login').hide();
        loginTime=0;
        if(signupTime==0){
            $('#section-register').show();
            signupTime=1;
        }else{
            $('#section-register').hide();
            signupTime=0;
        }
    }); 
});