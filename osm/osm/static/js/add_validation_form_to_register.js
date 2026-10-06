console.log("add")
document.getElementById("register_form1").addEventListener("submit", function(e){
   alert("Validation running");  
    
    
    let valid = true;

    // Clear previous errors
    document.getElementById("username_error").innerHTML = "";
    document.getElementById("user_email_error").innerHTML = "";
    document.getElementById("password_error").innerHTML = "";
    document.getElementById("confirm_password_error").innerHTML = "";
    document.getElementById("group_id_error").innerHTML = "";
    let username = document.getElementById("username1").value.trim();
    let password = document.getElementById("password1").value.trim();
    let confirm_password = document.getElementById("confirm_password1").value.trim();
    let email = document.getElementById("email1").value.trim();
    let group_id = document.getElementById("group_id1").value.trim();
    
//group  validation
if(group_id !== "2" && group_id !=="3"){
        document.getElementById("group_id_error").innerHTML = "choose as student or Teacher";
        valid = false;
         e.preventDefault();
    }
//user name validation
  if(username === ""){
        document.getElementById("username_error").innerHTML = " UserName is required";
        valid = false;
         e.preventDefault();}
  else if(!/^[A-Za-z ]+$/.test(username)){
        document.getElementById("username_error").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();}

    
    //  user Email Validation
    if(email === ""){
        document.getElementById("user_email_error").innerHTML = "Email is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
        document.getElementById("user_email_error").innerHTML = "Invalid email format";
        valid = false;
         e.preventDefault();
    }

   

    // user password validation
    if(password=== ""){
        document.getElementById("password_error").innerHTML = "Password is required";
        valid = false;
         e.preventDefault();
    }
    else if(password.length<8) {
        document.getElementById("password_error").innerHTML = "Password contain aleast 8 chareacters";
        valid = false;
         e.preventDefault();

    }
    if(confirm_password=== ""){
        document.getElementById("confirm_password_error").innerHTML = " Confirm Password is required";
        valid = false;
         e.preventDefault();
    }
    else if(confirm_password.length<8) {
        document.getElementById("confirm_password_error").innerHTML = " Confirm Password contain aleast 8 chareacter";
        valid = false;
         e.preventDefault();

    }
    

    
    
    
    

    if(!valid){
        e.preventDefault();
    }
});