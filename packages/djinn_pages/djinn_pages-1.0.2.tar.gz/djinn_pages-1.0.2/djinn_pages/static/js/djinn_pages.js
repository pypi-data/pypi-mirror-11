$(document).ready(function(){
    resizeDiv();
});

window.onresize = function(event) {
    resizeDiv();
}

function resizeDiv() {
    head_offset = $(".fullbox").offset();
    if (head_offset){
        headheight = head_offset.top;
    } else {
        headheight = 0;
    }
    vph = $(window).height()-headheight-1;
    $(".fullbox").css({"height": vph});
}