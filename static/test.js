/*(document).ready(function() {

   alert("hello world!");
);*/

/*alert("first hello world!");*/

var namesp = namesp || {};
var isFirstLoad = function(namesp) {
   var isFirst = namesp.firstLoad === undefined;
   console.log("isFirst is: " + isFirst);
   namesp.firstLoad = false;
   if (!isFirst) {
       console.log("warning, this file has been loaded more than once.");
    }
   return isFirst;
 };
if (!isFirstLoad(namesp)) {
    console.log("this conditional was activated");
    throw new Error("something went wrong");
 } else {
    console.log(isFirstLoad(namesp));
    console.log("failure to identify isFirstLoad as false");
  }
alert("hello world");
