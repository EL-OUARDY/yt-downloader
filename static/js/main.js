$(function () {
  // document is ready

  // download button click
  $("#download").on("click", () => {
    // check if url entered
    if ($("#url").val() == "") return

    // send AJAX request to server /details endpoint to get video informatio
    $.get("/details", { url: $("#url").val() }, function (data) {
      console.log(data);
      $("#video-card img").attr("src", data.thumbnail)
      $("#video-card .title").html(data.title)
      $("#video-card .views").html(data.views + " views")
      $("#video-card .length").html(formatDuration(data.length))
      $("#video-card").fadeIn("slow")
    });
  })


  // function to format video duration
  function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  }
});
