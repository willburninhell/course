$("a[rel^='menu']").click(function (event) {
    event.preventDefault();
    var key = $(this).attr("name");
    var k = key.split("/");
    $("#content").text("Загружаю...");
    switch(k[0]){
        case "users":
            var path="//127.0.0.1:8000/clients/"+k[1]+"/"+k[2]+"/";
            break;

        case "ports":
            var path="//127.0.0.1:8000/ports/"+k[1]+"/"+k[2]+"/";
            break; 

        case "switches":
            var path="//127.0.0.1:8000/switches/"+k[1]+"/"+k[2]+"/";
            break;

        case "macs":
            var path="//127.0.0.1:8000/macs/"+k[1]+"/"+k[2]+"/";
            break; 
    }
    $("#content").load(path);
});