function toggle_display(obj){var el=document.getElementById(obj);if(el.style.display!="none"){el.style.display="none"}else{el.style.display=""}}
function style_display_hide(obj){var el=document.getElementById(obj);el.style.display="none"}
function style_display_show(obj){var el=document.getElementById(obj);el.style.display=""}
function switchimg(obj,src1,src2){var el=document.getElementById(obj);el.src=(el.src==src1)?src2:src1}
function open_courses_toggle(i){el=document.getElementById(i);clas=el.getAttribute("class");replace=clas.replace("tree_closed","tree_opened");if(replace==clas)
replace=clas.replace("tree_opened","tree_closed");el.setAttribute("class",replace)}