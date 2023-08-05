function InitPalette() {
    $(".toggle-palette a").click(function(){
        $(".palette").toggleClass("open");
     });
}

function reset_btn(){
    $(".palette a.reset").click(function() {
        $( "#navigation" ).insertAfter( "#header" );
    });
}

function move_menubottom() {
    $(".palette .header-special .add-menu-bottom").click(function(){
        $( "#navigation" ).insertAfter( "#carousel-wrapper" );
     });
}

function carousel_clear() {
$(".palette .header-special .add-carousel-clear").click(function(){
    if($("#carousel-wrapper.container").length>0){
        $( "#carousel-wrapper" ).removeClass("container");
        $( "#carousel-wrapper .carousel-inner" ).removeClass("col-md-12");
    }
    else {
        $( "#carousel-wrapper" ).addClass("container");
        $( "#carousel-wrapper .carousel-inner" ).addClass("col-md-12");
    }

 });
}

function Add_header_normal() {
    $(".palette .headers ul li a.add-header-normal").click(function(){
         $("body").removeClass(" header-both header-light header-dark ");
         $("body").addClass("header-normal");
     });
}

function Add_header_dark() {
    $(".palette .headers ul li a.add-header-dark").click(function(){
         $("body").removeClass("header-light header-normal header-both")
         $("body").addClass("header-dark");
     });
}

function Add_header_light() {
    $(".palette .headers ul li a.add-header-light").click(function(){
         $("body").removeClass("header-normal header-dark header-both")
         $("body").addClass("header-light");
     });
}

function Add_header_both() {
    $(".palette .headers ul li a.add-header-both").click(function(){
         $("body").removeClass("header-light header-dark header-normal")
         $("body").addClass("header-both");
     });
}

function Checkpalette() {
    if(!$(".menu-palette").length>0){
        $(".palette").remove();
    }
}

$(document).ready(function() {
    carousel_clear();
    Checkpalette();
    InitPalette();
    Add_header_normal();
    Add_header_light();
    Add_header_dark();
    Add_header_both();
    move_menubottom();
    reset_btn();
});
