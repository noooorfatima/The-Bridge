<?php
   echo 'beep';
   $name     = $_POST['name'];
   $email    = $_POST['email'];
   $message  = $_POST['message'];
   $from     = 'From: Bridge Dev';
   $to       = 'demery@haverford.edu';
   $subject  = 'Oh hey there';
   if ($_POST['submit']){
     if (mail ($to, $subject, $body, $from)) {
       echo '<p>Your message has been sent!</p>';
     } else {
         echo '<p>Something went wrong, go back and try again!</p>';
     }
   }
?> 
