// From : https://codepen.io/abdulqudus001/pen/rNORJYo

// PDF Upload
const handlePdfUpload = async (formData) => {
  const res = await fetch("/questions/process-pdf/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  Swal.fire({
    title: "در حال پردازش فایل...",
    html: `
            <div>منتظر بمون</div>
            <div style="margin-top:10px;font-size:14px;color:#666">
                این عملیات ممکنه چند ثانیه طول بکشه...
            </div>
        `,
    allowOutsideClick: false,
    allowEscapeKey: false,
    showConfirmButton: false,
    didOpen: () => Swal.showLoading(),
  });

  const timer = setInterval(async () => {
    const r = await fetch(`/questions/process-pdf-status/${data.task_id}`);

    const contentType = r.headers.get("content-type");

    if (contentType && contentType.includes("text/html")) {
      clearInterval(timer);
      Swal.close();

      document.open();
      document.write(await r.text());
      document.close();
      return;
    }

    const status = await r.json();

    if (status.status !== "processing") {
      clearInterval(timer);
      Swal.close();
    }
  }, 2000);
};

const file = document.querySelector("#pdf_file");
file.addEventListener("change", (e) => {
  const upload_form = document.getElementById("upload_form");

  const formData = new FormData(upload_form);

  handlePdfUpload(formData);
});
