
document.getElementById("teacher_leave").addEventListener("submit", function(e){
    console.log('valid')
    
    
    
    let valid = true;

    // Clear previous errors
    document.getElementById("teacher_id_error").innerHTML = "";
    document.getElementById("first_name_error").innerHTML = "";
    document.getElementById("last_name_error").innerHTML = "";
    document.getElementById("reason_error").innerHTML = "";
    document.getElementById("ph_no_error").innerHTML = "";
    document.getElementById("date_error").innerHTML = "";
     

     let tid = document.getElementById("teacher_id").value.trim();
    let first_name = document.getElementById("first_name").value.trim();
    let last_name = document.getElementById("last_name").value.trim();
    let reason = document.getElementById("reason").value.trim();
    let phone = document.getElementById("ph_no").value.trim();
    let date = document.getElementById("date").value.trim();
    
    

//date validation
if(date === ""){
        document.getElementById("date_error").innerHTML = "Date is required";
        valid = false;
         e.preventDefault();
    }
    
   
// Teacher ID Validation
    if(tid === ""){
        document.getElementById("teacher_id_error").innerHTML = "Teacher id is required";
        valid = false;
         e.preventDefault();
    }
    
   
    //Teacher Name Validation
    if(first_name === ""){
        document.getElementById("first_name_error").innerHTML = "First Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(first_name)){
        document.getElementById("first_name_error").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    if(last_name === ""){
        document.getElementById("last_name_error").innerHTML = " Last Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(last_name)){
        document.getElementById("last_name_error").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    // Phone Validation
    if(phone=== ""){
        document.getElementById("ph_no_error").innerHTML = "Phone number is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[6-9]\d{9}$/.test(phone)){
        document.getElementById("ph_no_error").innerHTML ="Enter a valid 10-digit phone number";
        valid = false;
         e.preventDefault();
    }
    //validation for reason
    if (reason ===""){
        document.getElementById("reason_error").innerHTML="Please specified any valid reason";
      e.preventDefault();
    }
   
    
    

    if(!valid){
        e.preventDefault();
    }
});