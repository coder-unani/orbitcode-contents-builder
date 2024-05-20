const frmSearch = document.forms.frmSearch;
const frmSave = document.forms.frmSave;
const idSearch = document.querySelector('#idSearch');
const idSave = document.querySelector('#idSave');
const idViewMode = document.querySelector('#idViewMode');
const loading = document.querySelector('#id_loading');
idSearch.addEventListener("click", function(e) {
    e.preventDefault();
    if (confirm("데이터를 불러오겠습니다.?\n다소 시간이 소요될 수 있습니다.")) {
        loading.classList.remove('hidden');
        frmSearch.parser.value = "on";
        frmSearch.submit();
    }
});
if (idViewMode !== null) {
    idViewMode.addEventListener("click", function(e) {
        e.preventDefault();
        loading.classList.remove('hidden');
        const view_mode = frmSearch.view_mode.value;
        if (view_mode == "html") {
            view_mode = "json"
        } else {
            view_mode = "html"
        }
        frmSearch.view_mode.value = view_mode;
        frmSearch.submit();
    });
}

if (idSave !== null) {
    idSave.addEventListener("click", function(e) {
        e.preventDefault();
        loading.classList.remove('hidden');
        if (confirm("데이터를 DB에 저장합니다.")) {
            frmSave.submit();
        }
    });
}