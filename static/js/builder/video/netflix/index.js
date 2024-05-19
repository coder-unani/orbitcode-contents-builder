frmSearch = document.forms.frm_search;
frmContents = document.forms.frm_contents;

formFieldIds = document.querySelector("input[name=search_ids]");
searchFiledIds = document.querySelector("#input_search_ids");
displayFieldIds = document.querySelector("#div_ids_field");

if (searchFiledIds !== null) {
    searchFiledIds.addEventListener("keydown", function (e) {
        if (e.keyCode === 13) {
            applyFormFieldIds();
        }
    });
}

btnAddIds = document.querySelector("#btn_add_ids");
btnAddIds.addEventListener("click", function (e) {
    e.preventDefault();
    applyFormFieldIds();
});

btnFrmSearch = document.querySelector("#btn_frm_search");
if (btnFrmSearch !== null) {
    btnFrmSearch.addEventListener("click", function (e) {
        e.preventDefault();
        frmSearch.submit();
    });
}

btnFrmSubmit = document.querySelector("#btn_frm_submit");
if (btnFrmSubmit !== null) {
  btnFrmSubmit.addEventListener("click", function (e) {
    e.preventDefault();

    contentIds = document.querySelector("input[name=content_ids]").value;
    if (contentIds === null) {
      alert("선택된 데이터가 없습니다.");
      return;
    }

    console.log(contentIds);

    contentIdsToArray = contentIds.split(",");
    for (let i = 0; i < contentIdsToArray.length; i++) {
      contentType = document.querySelector("input[name=content_kind_" + contentIdsToArray[i] + "]:checked");
      
      if (contentType === null) {
        alert("컨텐츠의 타입이 선택되지 않은 데이터가 있습니다: " + contentIdsToArray[i]);
        return;
      }
    }

    frmContents.submit();
  });
}

const applyFormFieldIds = () => {
    // Id 출력영역 초기화
    displayFieldIds.innerHTML = "";
    // 입력받은 검색Id 가져오기
    arrSearchFiledIds = searchFiledIds.value.split(",");
    // 기존에 등록된 Id 가져오기
    arrValidIds = formFieldIds.value.split(",");
    // 입력받은 검색Id loop 돌며 기존에 등록된 Id와 중복체크
    arrSearchFiledIds.map((id) => {
         console.log("id=" + id);
        if (arrValidIds.indexOf(id) < 0 && id.length > 0) {
            arrValidIds.push(id);
        }
    });
    
    // 최종적으로 검색될 Id 출력
    arrFormFiledIds = [];
    arrValidIds.map((id) => {
        if (id.length > 0) {
            arrFormFiledIds.push(id);
            let spanId = document.createElement("span");
            spanId.setAttribute("id", "span_id_" + id);
            spanId.setAttribute("class", "py-1 pl-3 pr-2 mr-1 text-white bg-slate-300 rounded-xl");
            spanId.innerHTML = id;
            spanId.innerHTML += "<span class='ml-1 text-white' onclick='deleteFormIds(" + id + ")'>X</span>";
            displayFieldIds.appendChild(spanId);
        }
    });
    // Form Id변수 업데이트
    formFieldIds.value = arrFormFiledIds.join(",");
    // 검색Id필드 초기화
    searchFiledIds.value = "";
    // 가져오기 버튼 활성화
    if (formFieldIds.value.length > 0) {
        btnFrmSearch.classList.remove("hidden");
    } else {
        btnFrmSearch.classList.add("hidden");
    }
}

const deleteFormIds = (id) => {
    arrFormFiledIds = formFieldIds.value.split(",");
    arrFormFiledIds.map((value, index) => {
        if (value == id) {
            arrFormFiledIds.splice(index, 1);
        }
    });

    formFieldIds.value = arrFormFiledIds.join(",");
    applyFormFieldIds();
}