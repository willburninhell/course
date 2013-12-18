$("a[rel^='ids']").click(function (event) {
    event.preventDefault();
    var host=$(location).attr('host');
    var addr=$(this).attr('id').split("/");
    var path="//127.0.0.1:8000/clients/"+addr[0]+"/"+addr[1]+"/";
    $("#content").text("Загружаю...");
    $("#content").load(path);
});