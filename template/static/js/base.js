/**
 * Created by yangxj on 16/8/9.
 */
function showImg(url,docid) {
    console.log(url + ":" + docid);
    var frameid = 'frameimg' + docid.toString();
    window.img = '<img id="img" src=\''+url+'?'+Math.random()+'\' width=100%/><script>window.onload = function() { parent.document.getElementById(\''+frameid+'\').height = document.getElementById(\'img\').height+\'px\'; }<'+'/script>';
    console.log("frameid:" + frameid);
    document.getElementById(frameid).innerHTML = ('<iframe id="'+frameid+'" src="javascript:parent.img;" frameBorder="0" scrolling="no" width="100%"></iframe>');
}

$(function() {
    var fix = $('.fixed');                      //滚动悬浮块
    var end = $('.bottom');                     //滚动到这个元素后结束固定
    var fixTop = fix.offset().top,    //滚动悬浮块与顶部的距离
        fixHeight = fix.height();     //滚动悬浮块高度
    var endTop, miss;    //结束元素与顶部的距离

    $(window).scroll(function() {
        //页面与顶部高度
        var docTop = Math.max(document.body.scrollTop, document.documentElement.scrollTop);

        //如果有结束滚动块
        if (end.length > 0) {
            endTop = end.offset().top;
            miss = endTop - docTop - fixHeight;
        }

        if (fixTop < docTop) {
            fix.css({'position': 'fixed'});
            if ((end.length > 0) && (endTop < (docTop + fixHeight))) {
                fix.css({top: miss});           //滚动悬浮块滑到结束块上时，top值为负，即慢慢隐藏出浏览器
            } else{
                fix.css({top: 0});              //滚动悬浮块未到结束块上时，top为0
            }
        } else {
            fix.css({'position': 'static'});
        }
    })
});


