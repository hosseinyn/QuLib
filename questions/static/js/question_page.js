// Display pdf

const canvas = document.getElementById("pdf-canvas");
const url = canvas.dataset.url;

pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.9.179/pdf.worker.min.js";

pdfjsLib.getDocument(url).promise.then((pdf) => {
  pdf.getPage(1).then((page) => {
    const viewport = page.getViewport({ scale: 1.5 });
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    page.render({ canvasContext: canvas.getContext("2d"), viewport });
  });
});

// Convert pdf to word
const handleConvert = async () => {
  const convertBtn = document.getElementById("convert-btn");

  const formData = new FormData();
  formData.append("question_id", convertBtn.dataset.question);

  const res = await fetch("/questions/convert-to-word/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  Swal.fire({
    title: "در حال تبدیل فایل...",
    html: `
        <div>منتظر بمون</div>
        <div style="margin-top:10px;font-size:14px;color:#666">
            این عملیات ممکنه چند ثانیه طول بکشه...
        </div>
    `,
    allowOutsideClick: false,
    allowEscapeKey: false,
    showConfirmButton: false,
    didOpen: () => {
        Swal.showLoading();
    }
});

  const timer = setInterval(async () => {
    const r = await fetch(`/questions/convert-to-word-status/${data.task_id}`);

    const contentType = r.headers.get("content-type");

    if (
      contentType &&
      contentType.includes(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      )
    ) {
      clearInterval(timer);

      const blob = await r.blob();

      const url = URL.createObjectURL(blob);

      const disposition = r.headers.get("Content-Disposition");

      let filename = "نمونه سوال.docx";

      if (disposition) {
        const match = disposition.match(
          /filename\*=UTF-8''([^;]+)|filename="?([^"]+)"?/i,
        );

        if (match) {
          filename = decodeURIComponent(match[1] || match[2]);
        }
      }

      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();

      URL.revokeObjectURL(url);
      Swal.close()
      return;
    }

    const status = await r.json();

    if (status.status !== "processing") {
      clearInterval(timer);
    }
  }, 2000);
};
