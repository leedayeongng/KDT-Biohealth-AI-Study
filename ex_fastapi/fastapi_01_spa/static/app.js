const apiUrl = '/items/'; // 백엔드 기본 엔드포인트 변경됨 (01_fastapi_restful_py 와 동일)
let isEditing = false;

document.addEventListener('DOMContentLoaded', fetchItems);

// 1. Read All (GET)
async function fetchItems() {
    try {
        const response = await fetch(apiUrl);
        const items = await response.json();
        renderItems(items);
    } catch (error) {
        console.error('아이템 조회 에러:', error);
    }
}

function renderItems(items) {
    const listDiv = document.getElementById('item-list');
    listDiv.innerHTML = '';

    if (items.length === 0) {
        listDiv.innerHTML = '<p style="color:#777;">등록된 아이템이 없습니다.</p>';
        return;
    }

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';

        const descText = item.description ? ` | 설명: ${item.description}` : '';

        itemDiv.innerHTML = `
            <div class="item-details">
                <span class="item-title">ID: ${item.id} - ${item.name}</span>
                <span class="item-meta">가격: ${item.price} ₩ ${descText}</span>
            </div>
            <div>
                <button class="edit-btn" onclick="editItem(${item.id}, '${item.name}', '${item.description || ''}', ${item.price})">수정</button>
                <button class="delete-btn" onclick="deleteItem(${item.id})">삭제</button>
            </div>
        `;
        listDiv.appendChild(itemDiv);
    });
}

// 2. Create(POST) or Update(PUT) 분기
async function submitForm() {
    const idInput = document.getElementById('item-id');
    const nameInput = document.getElementById('item-name');
    const descInput = document.getElementById('item-desc');
    const priceInput = document.getElementById('item-price');

    const id = parseInt(idInput.value);
    const name = nameInput.value.trim();
    const desc = descInput.value.trim();
    const price = parseFloat(priceInput.value);

    if (isNaN(id) || !name || isNaN(price)) {
        alert("ID, 이름, 가격은 필수 항목입니다.");
        return;
    }

    const payload = {
        id: id,
        name: name,
        description: desc || null,
        price: price
    };

    try {
        const method = isEditing ? 'PUT' : 'POST';
        const url = isEditing ? `${apiUrl}${id}` : apiUrl;

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            resetForm();
            fetchItems();
        } else {
            const errorData = await response.json();
            alert("Error: " + errorData.detail);
        }
    } catch (error) {
        console.error('요청 처리 에러:', error);
    }
}

// 3. Delete (DELETE)
async function deleteItem(id) {
    if (!confirm(`정말 ID ${id} 아이템을 삭제하시겠습니까?`)) return;
    try {
        const response = await fetch(`${apiUrl}${id}`, { method: 'DELETE' });
        if (response.ok) {
            fetchItems();
        } else {
            const errorData = await response.json();
            alert("삭제 실패: " + (errorData.detail || "알 수 없는 오류"));
        }
    } catch (error) {
        console.error('삭제 에러:', error);
    }
}

// 4. Update 폼 준비
function editItem(id, name, desc, price) {
    document.getElementById('item-id').value = id;
    document.getElementById('item-id').disabled = true; // ID 변경 불가
    document.getElementById('item-name').value = name;
    document.getElementById('item-desc').value = desc;
    document.getElementById('item-price').value = price;

    document.getElementById('submit-btn').innerText = "아이템 수정";
    document.getElementById('form-title').innerText = "아이템 수정 모드";
    document.getElementById('cancel-btn').style.display = "inline-block";

    isEditing = true;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('item-id').value = '';
    document.getElementById('item-id').disabled = false;
    document.getElementById('item-name').value = '';
    document.getElementById('item-desc').value = '';
    document.getElementById('item-price').value = '';

    document.getElementById('submit-btn').innerText = "아이템 추가";
    document.getElementById('form-title').innerText = "새 아이템 추가";
    document.getElementById('cancel-btn').style.display = "none";

    isEditing = false;
}
