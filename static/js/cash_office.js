// Cash Office Portal - Drawer and PIN Verification Handler
(function() {
    function initCashOffice() {
        console.log('[CashOffice] Initializing Cash Office Drawer & PIN Modal...');

        // Elements
        var btnOpenDrawer = document.getElementById('btn-open-drawer');
        var btnCloseDrawer = document.getElementById('btn-close-drawer');
        var drawer = document.getElementById('check-offcanvas-drawer');
        var drawerOverlay = document.getElementById('drawer-overlay');

        function openDrawer() {
            if (drawerOverlay && drawer) {
                drawerOverlay.style.display = 'block';
                setTimeout(function() {
                    drawerOverlay.style.opacity = '1';
                    drawer.style.right = '0';
                }, 10);
            }
        }

        function closeDrawer() {
            if (drawerOverlay && drawer) {
                drawer.style.right = '-550px';
                drawerOverlay.style.opacity = '0';
                setTimeout(function() {
                    drawerOverlay.style.display = 'none';
                }, 350);
            }
        }

        if (btnOpenDrawer) {
            btnOpenDrawer.addEventListener('click', openDrawer);
        }
        if (btnCloseDrawer) {
            btnCloseDrawer.addEventListener('click', closeDrawer);
        }
        if (drawerOverlay) {
            drawerOverlay.addEventListener('click', closeDrawer);
        }

        // Auto open drawer if search query parameter exists
        try {
            var urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('q') || urlParams.has('status')) {
                openDrawer();
            }
        } catch (e) {}

        // PIN Verification Modal Elements
        var modalOverlay = document.getElementById('pin-modal-overlay');
        var btnCloseModal = document.getElementById('btn-close-modal');
        var btnDoneModal = document.getElementById('btn-done-modal');
        var modalStatePin = document.getElementById('modal-state-pin');
        var modalStateUnlocked = document.getElementById('modal-state-unlocked');
        var pinForm = document.getElementById('pin-verification-form');
        var pinInput = document.getElementById('input-pin-code');
        var pinErrorAlert = document.getElementById('pin-error-alert');
        var pinErrorText = document.getElementById('pin-error-text');

        function openPinModal(checkId, payeeName, dvNumber) {
            if (!modalOverlay || !pinInput) return;
            var inputId = document.getElementById('modal-check-id');
            var elPayee = document.getElementById('modal-payee-name');
            var elDv = document.getElementById('modal-dv-number');
            
            if (inputId) inputId.value = checkId;
            if (elPayee) elPayee.textContent = payeeName;
            if (elDv) elDv.textContent = 'DV #' + dvNumber;
            
            pinInput.value = '';
            if (pinErrorAlert) pinErrorAlert.style.display = 'none';
            if (modalStatePin) modalStatePin.style.display = 'block';
            if (modalStateUnlocked) modalStateUnlocked.style.display = 'none';
            
            modalOverlay.style.display = 'flex';
            setTimeout(function() {
                pinInput.focus();
            }, 100);
        }

        function closeModal() {
            if (!modalOverlay) return;
            modalOverlay.style.display = 'none';
            var elAmt = document.getElementById('unlocked-amount');
            if (elAmt) elAmt.textContent = '₱0.00';
            if (pinInput) pinInput.value = '';
            if (pinErrorAlert) pinErrorAlert.style.display = 'none';
            if (modalStateUnlocked) modalStateUnlocked.style.display = 'none';
            if (modalStatePin) modalStatePin.style.display = 'block';
        }

        if (btnCloseModal) btnCloseModal.addEventListener('click', closeModal);
        if (btnDoneModal) btnDoneModal.addEventListener('click', closeModal);
        if (modalOverlay) {
            modalOverlay.addEventListener('click', function(e) {
                if (e.target === modalOverlay) closeModal();
            });
        }

        // Delegate event listeners for all check cards and unlock buttons
        document.addEventListener('click', function(e) {
            var btnUnlock = e.target.closest('.btn-unlock-pin');
            if (btnUnlock) {
                e.preventDefault();
                e.stopPropagation();
                var checkId = btnUnlock.getAttribute('data-check-id');
                var payee = btnUnlock.getAttribute('data-payee');
                var dv = btnUnlock.getAttribute('data-dv');
                openPinModal(checkId, payee, dv);
                return;
            }

            var card = e.target.closest('.check-card-container');
            if (card) {
                e.preventDefault();
                var checkId = card.getAttribute('data-check-id');
                var payee = card.getAttribute('data-payee');
                var dv = card.getAttribute('data-dv');
                openPinModal(checkId, payee, dv);
            }
        });

        // Submit PIN Verification
        if (pinForm) {
            pinForm.addEventListener('submit', function(e) {
                e.preventDefault();
                var checkId = document.getElementById('modal-check-id').value;
                var pinCode = pinInput.value.trim();

                if (!pinCode) {
                    if (pinErrorText) pinErrorText.textContent = 'Please enter your 6-digit PIN password.';
                    if (pinErrorAlert) pinErrorAlert.style.display = 'block';
                    return;
                }

                var btnSubmit = document.getElementById('btn-submit-pin');
                if (btnSubmit) {
                    btnSubmit.disabled = true;
                    btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verifying PIN...';
                }

                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = cookies[i].trim();
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }

                fetch('/office/cash-office/verify-pin/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') || ''
                    },
                    body: JSON.stringify({
                        check_id: checkId,
                        pin_code: pinCode
                    })
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(res) {
                    if (btnSubmit) {
                        btnSubmit.disabled = false;
                        btnSubmit.innerHTML = '<i class="fa-solid fa-lock-open"></i> Verify PIN & View Transaction';
                    }

                    if (res.success && res.data) {
                        var data = res.data;
                        document.getElementById('unlocked-amount').textContent = data.amount;
                        document.getElementById('unlocked-payee').textContent = data.payee_name;
                        document.getElementById('unlocked-dv').textContent = data.voucher_number;
                        document.getElementById('unlocked-check-no').textContent = data.check_number;
                        document.getElementById('unlocked-date').textContent = data.check_date;
                        document.getElementById('unlocked-release-date').textContent = data.date_released;
                        document.getElementById('unlocked-requirements').textContent = data.claiming_requirements;

                        if (data.remarks && data.remarks !== 'None') {
                            document.getElementById('unlocked-remarks').textContent = data.remarks;
                            document.getElementById('unlocked-remarks-box').style.display = 'block';
                        } else {
                            document.getElementById('unlocked-remarks-box').style.display = 'none';
                        }

                        var badgeHtml = '';
                        if (data.claim_status === 'ready') {
                            badgeHtml = '<span style="background: #10b981; color: white; padding: 0.35rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;"><i class="fa-solid fa-circle-check"></i> READY FOR PICK-UP</span>';
                        } else if (data.claim_status === 'processing') {
                            badgeHtml = '<span style="background: #f59e0b; color: white; padding: 0.35rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;"><i class="fa-solid fa-clock"></i> IN PROCESSING</span>';
                        } else if (data.claim_status === 'released') {
                            badgeHtml = '<span style="background: #6b7280; color: white; padding: 0.35rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;"><i class="fa-solid fa-check-double"></i> RELEASED</span>';
                        } else {
                            badgeHtml = '<span style="background: #ef4444; color: white; padding: 0.35rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;"><i class="fa-solid fa-ban"></i> CANCELLED</span>';
                        }
                        document.getElementById('unlocked-status-badge').innerHTML = badgeHtml;

                        if (modalStatePin) modalStatePin.style.display = 'none';
                        if (modalStateUnlocked) modalStateUnlocked.style.display = 'block';
                    } else {
                        if (pinErrorText) pinErrorText.textContent = res.message || 'Incorrect PIN password.';
                        if (pinErrorAlert) pinErrorAlert.style.display = 'block';
                    }
                })
                .catch(function(err) {
                    if (btnSubmit) {
                        btnSubmit.disabled = false;
                        btnSubmit.innerHTML = '<i class="fa-solid fa-lock-open"></i> Verify PIN & View Transaction';
                    }
                    if (pinErrorText) pinErrorText.textContent = 'Network or server error during verification.';
                    if (pinErrorAlert) pinErrorAlert.style.display = 'block';
                });
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCashOffice);
    } else {
        initCashOffice();
    }
})();
