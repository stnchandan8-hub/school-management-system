console.log("validation")
document.getElementById("teacher_form").addEventListener("submit", function(e){
    
    
    
    let valid = true;

    // Clear previous errors
    document.getElementById("teacher_id_error").innerHTML = "";
    document.getElementById("user_id_error").innerHTML = "";
    document.getElementById("first_name_error").innerHTML = "";
    document.getElementById("last_name_error").innerHTML = "";
    document.getElementById("mail_error").innerHTML = "";
    document.getElementById("age_error").innerHTML = "";
    document.getElementById("phone_error").innerHTML = "";
    document.getElementById("address_error").innerHTML="";



    let first_name = document.getElementById("first_name").value.trim();
    let last_name = document.getElementById("last_name").value.trim();
    let email = document.getElementById("mail").value.trim();
    let teacher_id = document.getElementById("teacher_id").value.trim();
    let user_id = document.getElementById("user_id").value.trim();
    let phone = document.getElementById("contactno").value.trim();
   
    let address = document.getElementById("address").value.trim();
    let age = document.getElementById("age").value.trim();
   
   
    


    // Name Validation
    if(user_id === ""){
        document.getElementById("user_id_error").innerHTML = "user id is required";
        valid = false;
         e.preventDefault();
    }
    if(first_name === ""){
        document.getElementById("first_name_error").innerHTML = "Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(first_name)){
        document.getElementById("first_name_error").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    if(last_name === ""){
        document.getElementById("last_name_error").innerHTML = "Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(last_name)){
        document.getElementById("last_name_error").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }

    // Email Validation
    if(email === ""){
        document.getElementById("mail_error").innerHTML = "Email is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
        document.getElementById("mail_error").innerHTML = "Invalid email format";
        valid = false;
         e.preventDefault();
    }

    // teacher ID Validation
    if(teacher_id === ""){
        document.getElementById("teacher_id_error").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^\d+$/.test(teacher_id)){
        document.getElementById("teacher_id_error").innerHTML = "ID must contain only numbers";
        valid = false;
         e.preventDefault();
    }

    // Phone Validation
    if(phone === ""){
        document.getElementById("phone_error").innerHTML = "Phone number is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[6-9]\d{9}$/.test(phone)){
        document.getElementById("phone_error").innerHTML ="Enter a valid 10-digit phone number";
        valid = false;
         e.preventDefault();
    }
    

    
    
    //address validation
    if (address === "") {
        document.getElementById("address_error").innerHTML = "Address is required";
        valid = false;
         e.preventDefault();
    }
    else if (address.length < 10) {
        document.getElementById("address_error").innerHTML = "Address must be at least 10 characters";
        valid = false;
         e.preventDefault();
    }
    else if (!/^[A-Za-z0-9\s,.\-\/#]+$/.test(address)) {
         document.getElementById("address_error").innerHTML = "Enter a valid address";
        
        valid = false;
         e.preventDefault();
    }
    if (age ===""){
        document.getElementById("age_error").innerHTML="Age is required";
      e.preventDefault();
    }
    else if (parseInt(age)<=18 || parseInt(age)>60){
        document.getElementById("age_error").innerHTML="Age  must be range between (18-60)";
         e.preventDefault();
    }

    
    console.log("valid =", valid);

    if(!valid){
        e.preventDefault();
    }
});