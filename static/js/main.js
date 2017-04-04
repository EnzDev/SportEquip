$( function(){

  // Location autocomplete
  $("input.loc")[0].oninput = function(){
    let search = $(this).val();
    let act = $("input.act").val();
    if(search.length > 0){
      if(isFinite(search[0])){search = search.split(" ")[0]}
      $.getJSON("api/sport/city?city="+search+(act===""?"":"&act="+act)).done(function(d){
        var list = [];
        if(isFinite(search[0])){
        // Display POSTCODE - City
          list = d.map(function(i){return i.ComCode + " " + i.ComLib})
        }else{
        // Display City
          list = d.map(function(i){return i.ComLib})
        }

        list = new Set(list);
        $("datalist#loc").empty();
        for(c of list) $("datalist#loc").append('<option value="'+ c +'">')
      })
    }
  };

  // Activities autocomplete
  $("input.act")[0].oninput = function(){
    let search = $(this).val();
    let city = $("input.loc").val();
    let range = $("input.ran").val();
    if(isFinite(city[0])){city = city.split(" ")[0]}
    if(search.length > 0){
      $.getJSON("api/sport/activity?act="+search+(city===""?"":"&city="+city)+(range===""?"":"&range="+range)).done(function(d){
        let list = new Set(d);

        $("datalist#act").empty();
        for(c of list) $("datalist#act").append('<option value="'+ c +'">')
      })
    }
  }

  $("#search").click(function(){
    let act =   $("input.act").val();
    let city =  $("input.loc").val();
    let range = $("input.ran").val();

    query = []

    if(city!=="")  query.push("city="+city)
    if(range!=="") query.push("range="+range)
    if(act!=="")   query.push("act="+act)
    

    $.getJSON("api/sport/installation?"+query.join("&")).done(function(d){
        if(window.markers == undefined) window.markers=[];

        for(marker of window.markers){marker.remove()}

        bounds = [[undefined,undefined],[undefined,undefined]] // 
        $("#rightPanel ul").empty()

        sss = Object.keys(d).length>1 ? "s" : "";
        $("#nbResult").html(Object.keys(d).length +" résultat" + sss + " trouvé" + sss)

        for(noEquip in d){
          var equip = d[noEquip]

          $("<li>").html("<b>" + equip.EquNom + "</b><br>" + equip.Adresse[0]).appendTo($("#rightPanel ul"));

          if((bounds[0][0] == undefined || equip.EquGpsY < bounds[0][0] ) && (equip.EquGpsY!=0)) bounds[0][0] = equip.EquGpsY /* != 0 to prevent strange data */
          if((bounds[1][0] == undefined || equip.EquGpsY > bounds[1][0] ) && (equip.EquGpsY!=0)) bounds[1][0] = equip.EquGpsY

          if((bounds[0][1] == undefined || equip.EquGpsX < bounds[0][1] ) && (equip.EquGpsX!=0)) bounds[0][1] = equip.EquGpsX
          if((bounds[1][1] == undefined || equip.EquGpsX > bounds[1][1] ) && (equip.EquGpsX!=0)) bounds[1][1] = equip.EquGpsX

          window.markers.push( L.marker([equip.EquGpsY,equip.EquGpsX])
                          .addTo(map)
                          .bindPopup("<b>" + equip.EquNom + "</b><br>" + equip.Activite.join("<br>")) 
                      );
        }
        
        map.fitBounds(bounds);
      })

      if(range!="")
        $.post("api/sport/city", {"city":city}, function(d){
            if(window.range) window.range.remove()
            if  (range <= 3){
             window.range = L.circle([d[0], d[1]], 3*1000).addTo(map)
            }
            else{
            window.range = L.circle([d[0], d[1]], range*1000).addTo(map)
            }

        })

  })

});
