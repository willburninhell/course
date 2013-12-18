    $("a[rel^='chg']").click(function (event) {
        event.preventDefault();
        var path = "/ports/";
        var n = $(this).attr("name");
        console.log(n);
        var addr = n.split("/");
        var t = 'form[id="'+n+'"]';
        var data = $(t).serialize();
        console.log(data);
        var action = confirm('Вы уверены, что желаете внести изменения?');
        if(action){
            $.post( path, data, function() {
                $("#content").load("//127.0.0.1:8000/ports/"+addr[0]+'/'+addr[1]+'/');
            });
        }
    });