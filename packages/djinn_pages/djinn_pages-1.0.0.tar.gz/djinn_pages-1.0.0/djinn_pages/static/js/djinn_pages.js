$(document).ready(function(){
    resizeDiv();
});

window.onresize = function(event) {
    resizeDiv();
}

function resizeDiv() {
    headheight = $(".fullbox").offset().top;
    vph = $(window).height()-headheight-1;
    $(".fullbox").css({"height": vph});
}