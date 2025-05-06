window.onload = function () {
  const html5QrCode = new Html5Qrcode("reader");

  function onScanSuccess(decodedText, decodedResult) {
    document.getElementById("code").value = decodedText;
    html5QrCode.stop();
  }

  html5QrCode.start(
    { facingMode: "environment" },
    {
      fps: 10,
      qrbox: 250
    },
    onScanSuccess
  );

  document.getElementById("infoForm").addEventListener("submit", function (e) {
    e.preventDefault();
    fetch("/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: document.getElementById("code").value,
        name: document.getElementById("name").value,
        location: document.getElementById("location").value,
        status: document.getElementById("status").value,
        action: "Ažurirano ili dodano"
      })
    }).then(response => response.json()).then(data => {
      alert("Spremanje uspješno!");
      document.getElementById("infoForm").reset();
    });
  });
};