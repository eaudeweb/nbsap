$(function () {
    $(".print").on("click", function () {
       window.print();
    });

    $("input[type=text]:first").focus();

    var location = document.location.pathname;
    if(location.indexOf("staff") > 0) {
      $(".navbar").find(".staff_section").addClass("active");
    } else if(location.indexOf("country") > 0) {
      $(".navbar").find(".country_section").addClass("active");
    } else {
      $(".navbar").find(".meeting_section").addClass("active");
    }

    $(".delete-item").on("click", function (e) {
        e.preventDefault();
        var item = $(this).data("item");
        if(confirm("Are you sure you want to delete this " + item + "?")) {
          $.ajax({
            url: $(this).attr("href"),
            type: "DELETE",
            success: function (data) {
              data = $.parseJSON(data);
              document.location = data.url;
            }
          })
        }
      });

      // form events
    $("#file-input-container").on("change", "input[type=file]", function () {
        var form = $(this).parents("form");
        form.submit();
    });


  $(".upload-photo").on("click", function (e) {
    e.preventDefault();
    $("#file-input-container").slideToggle("fast");
  });

  // iframe events
  $("#file-input-iframe").load(function () {
    // after the upload is complete update the picture with the new one
    var data = $.parseJSON($(this).contents().text());

    if(data && data.status == "success") {
      $("#file-input-container").find(".err").text("").hide();
      $("#file-input-container").slideUp("fast");

      var img = $("#photo").find("img");
      if(!img.data("is_animated")) {
        img.fadeOut("slow", function () {
          $(this).attr("src", data.url).fadeIn("slow", function () {
            $(this).data("is_animated", false);
          });

          $(this).data("removed", false);
          $(".remove-photo").fadeIn("slow");
        });

        img.data("is_animated", true);
      }
    } else {
        $("#file-input-container").find(".err").text(data.error).show();
    }
  });

  $(".remove-photo").on("click", function(e) {
      e.preventDefault();
      if(!confirm("Are you sure you want to remove this picture?")) return;
      var self = $(this);
      $.ajax({
          url: $(this).attr("href"),
          type: "DELETE",
          success: function (data) {
              data = $.parseJSON(data);
              if(data && data.status == "success") {
                  $("#photo").find(".remove-photo").hide();
                  $("#photo").find("img").data("removed", true)
                             .fadeOut("slow", function () {
                                  $(this).attr("src", "");
                                  self.fadeOut("slow");
                               });
              }
          }
      });
    });


  $("#show-templates").on("click", function () {
    var templates = $("#templates")
    templates.slideToggle("fast");
    templates.find("input:first").focus()

    $(".sep").find(".icon-chevron-down, .icon-chevron-up")
             .toggleClass("icon-chevron-up")
             .toggleClass("icon-chevron-down");
  });

  $(".picker").ready(function(){
      var hidden_inputs = $(".picker").prev('input');
      var pickers = $(".picker");
      for (i=0; i<hidden_inputs.length; i++){
          var value_string = hidden_inputs[i].value.split("-").reverse().join(".");
          $(pickers[i]).val(value_string);
      }
  });
  $(".picker").datepicker({dateFormat: 'dd.mm.yy'})
  $(".picker").bind("change", function(year, month, inst){
            var display_string = $(this).val()
            var value_string = display_string.split('.').reverse().join('-')
            $(this).prev('input').attr({'value': value_string});
            $(this).val(function(index, value){
                return display_string;
            });
         })
});
