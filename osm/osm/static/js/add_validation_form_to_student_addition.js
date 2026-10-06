
document.getElementById("student_form").addEventListener("submit", function(e){
    
    
    
    let valid = true;

    // Clear previous errors
    document.getElementById("rollno1_error1").innerHTML = "";
    document.getElementById("first_name1_error1").innerHTML = "";
    document.getElementById("last_name1_error1").innerHTML = "";
    document.getElementById("cname1_error1").innerHTML = "";
    document.getElementById("gender1_error1").innerHTML = "";
    document.getElementById("address1_error1").innerHTML = "";
    document.getElementById("phone_number1_error1").innerHTML="";
    document.getElementById("s_email1_error1").innerHTML="";
    document.getElementById("s_age1_error1").innerHTML="";
    document.getElementById("pfn1_error1").innerHTML="";
    document.getElementById("pln1_error1").innerHTML="";
    document.getElementById("username_error").innerHTML="";





    let rollno = document.getElementById("rollno1").value.trim();
    let first_name = document.getElementById("first_name1").value.trim();
    let last_name = document.getElementById("last_name1").value.trim();
    let cname = document.getElementById("cname1").value.trim();
    let gender = document.getElementById("gender1").value.trim();
    let address = document.getElementById("address1").value.trim();
    let phone = document.getElementById("phone_number1").value.trim();
    let email= document.getElementById("s_email1").value.trim();
    let age = document.getElementById("s_age1").value.trim();
    let parent_first_name = document.getElementById("pfn1").value.trim();
    let parent_last_name = document.getElementById("pln1").value.trim();
    let username=document.getElementById("username").value.trim();
//gender validation
if (username==""){
    document.getElementById("username_error").innerHTML="Username is required"
    valid=false
    e.preventDefault();
}
if(gender === ""){
        document.getElementById("gender1_error1").innerHTML = "Gender is required";
        valid = false;
         e.preventDefault();
    }
    
   
// student ID Validation
    if(rollno === ""){
        document.getElementById("rollno1_error1").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^\d+$/.test(teacher_id)){
        document.getElementById("rollno1_error1").innerHTML = "ID must contain only numbers";
        valid = false;
         e.preventDefault();
    }
   
   
    
  //class name validation
  if(cname === ""){
        document.getElementById("cname1_error1").innerHTML = " Class Name is required";
        valid = false;
         e.preventDefault();}
  else if(!/^[A-Za-z ]+$/.test(cname)){
        document.getElementById("cname1_error1").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();}

    //parent Name Validation
    if(parent_first_name === ""){
        document.getElementById("pfn1_error1").innerHTML = "First Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(parent_first_name)){
        document.getElementById("pfn1_error1").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    if(parent_last_name === ""){
        document.getElementById("pln1_error1").innerHTML = " Last Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(parent_last_name)){
        document.getElementById("pln1_error1").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    //student name validation
    if(first_name === ""){
        document.getElementById("first_name1_error1").innerHTML = " First Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(first_name)){
        document.getElementById("first_name1_error1").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }
    if(last_name === ""){
        document.getElementById("last_name1_error1").innerHTML = "Last Name is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[A-Za-z ]+$/.test(last_name)){
        document.getElementById("last_name1_error1").innerHTML = "Only letters allowed";
        valid = false;
         e.preventDefault();
    }

    // Email Validation
    if(email === ""){
        document.getElementById("s_email1_error1").innerHTML = "Email is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
        document.getElementById("s_email1_error1").innerHTML = "Invalid email format";
        valid = false;
         e.preventDefault();
    }

   

    // Phone Validation
    if(phone=== ""){
        document.getElementById("phone_number1_error1").innerHTML = "Phone number is required";
        valid = false;
         e.preventDefault();
    }
    else if(!/^[6-9]\d{9}$/.test(phone)){
        document.getElementById("phone_number1_error1").innerHTML ="Enter a valid 10-digit phone number";
        valid = false;
         e.preventDefault();
    }
    

    
    
    //address validation
    if (address === "") {
        document.getElementById("address1_error1").innerHTML = "Address is required";
        valid = false;
         e.preventDefault();
    }
    else if (address.length < 10) {
        document.getElementById("address1_error1").innerHTML = "Address must be at least 10 characters";
        valid = false;
         e.preventDefault();
    }
    else if (!/^[A-Za-z0-9\s,.\-\/#]+$/.test(address)) {
         document.getElementById("address1_error1").innerHTML = "Enter a valid address";
        
        valid = false;
         e.preventDefault();
    }
    //validation for age
    if (age ===""){
        document.getElementById("s_age1_error1").innerHTML="Age is required";
      e.preventDefault();
    }
    else if (parseInt(age)<=60 || parseInt(age)>=7){
        document.getElementById("s_age1_error1").innerHTML="Age  must be range between (7 to 60 )";
         e.preventDefault();
    }

    
    console.log("valid =", valid);

    if(!valid){
        e.preventDefault();
    }
});