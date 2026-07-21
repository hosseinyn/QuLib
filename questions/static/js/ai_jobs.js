// Difficulty Detect
const handleDetectDifficulty = async () => {
  const form = document.getElementById("difficulty-detector");
  const formData = new FormData(form);

  const res = await fetch("/qulib-ai/difficulty-detector/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  Swal.fire({
    title: "داریم پردازش میکنیم...",
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
    const r = await fetch(
      `/qulib-ai/difficulty-detector-status/${data.task_id}`,
    );

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

// Create Same Question
const handleCreateSameQuestion = async () => {
  const form = document.getElementById("create-same-question");
  const formData = new FormData(form);

  const res = await fetch("/qulib-ai/create-same-question/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  Swal.fire({
    title: "داریم پردازش میکنیم...",
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
    const r = await fetch(
      `/qulib-ai/create-same-question-status/${data.task_id}`,
    );

    const contentType = r.headers.get("content-type");

    if (contentType && contentType.includes("text/html")) {
      clearInterval(timer);
      Swal.close();

      document.open();
      document.write(await r.text());
      document.close();
      window.addEventListener("load", () => {
        MathJax.typesetPromise();
      });
      return;
    }

    const status = await r.json();

    if (status.status !== "processing") {
      clearInterval(timer);
      Swal.close();
    }
  }, 2000);
};

// Solve Question
const handleSolveQuestion = async () => {
  const form = document.getElementById("solve-text");
  const formData = new FormData(form);

  const res = await fetch("/qulib-ai/solve-text/", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  Swal.fire({
    title: "داریم پردازش میکنیم...",
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
    const r = await fetch(
      `/qulib-ai/solve-text-status/${data.task_id}`,
    );

    const contentType = r.headers.get("content-type");

    if (contentType && contentType.includes("text/html")) {
      clearInterval(timer);
      Swal.close();

      document.open();
      document.write(await r.text());
      document.close();
      window.addEventListener("load", () => {
        MathJax.typesetPromise();
      });
      return;
    }

    const status = await r.json();

    if (status.status !== "processing") {
      clearInterval(timer);
      Swal.close();
    }
  }, 2000);
};