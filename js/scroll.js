function scrollToElement(elementId){
    $("html, #transcript").animate({
        scrollTop: $('#'+elementId).offset().top}, 0
    );
}

$().click(function (event){
    event.preventDefault();
    $('#transcript').scrollToElement();
});