console.log("add")
document.getElementById("login_form").addEventListener("submit", function(e){
   alert("Validation running");  
    
    
    let valid = true;

    // Clear previous errors
    document.getElementById("username_error2").innerHTML = "";
    document.getElementById("password_error2").innerHTML = "";
   
    let username = document.getElementById("username2").value.trim();
    let password = document.getElementById("password2").value.trim();
   
//user name validation
  if(username === ""){
        document.getElementById("username_error2").innerHTML = " UserName is required";
        valid = false;
         e.preventDefault();}
  else if(!/^[A-Za-z ]+$/.test(username)){
        document.getElementById("username_error2").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();}

    
    

   

    // user password validation
    if(password=== ""){
        document.getElementById("password_error2").innerHTML = "Password is required";
        valid = false;
         e.preventDefault();
    }
    else if(password.length<8) {
        document.getElementById("password_error2").innerHTML = "Password contain aleast 8 chareacter";
        valid = false;
         e.preventDefault();

    }
    
    

    
    
    
    

    if(!valid){
        e.preventDefault();
    }
});