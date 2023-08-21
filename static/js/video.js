var previousScrollPosition = 0; // ポップアップ表示前のスクロール位置を保存
var videoPlayer;

function showPopupVideo(videoPopupId) {
  var videoPopup = document.getElementById(videoPopupId);
  videoPlayer = document.getElementById("videoPlayer");

  // ポップアップ表示前のスクロール位置を記憶
      previousScrollPosition = window.scrollY;

  // ポップアップ表示する
  videoPopup.style.display = "block";
  videoPlayer.pause();
}

    // ポップアップを閉じるための関数
function closePopupVideo(videoPopupId) {
  var videoPopup = document.getElementById(videoPopupId);

  // ポップアップ表示前のスクロール位置に移動
      window.scrollTo(0, previousScrollPosition);

  // ポップアップを閉じる
  videoPopup.style.display = "none";
  videoPlayer.pause();

  // ビデオを再生
    playVideo();
}

// ビデオを再生する関数
function playVideo() {
  if (videoPlayer) { // videoPlayer 変数が存在する場合に再生
    videoPlayer.play();
  }
}






