"use strict";
var vm = new Vue({
    el: '#app',
    data: {
        json: {
            view: [],
            data: [],
            tags: [],
            likes: [],
            comments: [],
            prizesList: []
        },
        obj: {
            imgXhr: new XMLHttpRequest()
        },
        settings: {},
        default_settings: {
            fullScreen: false,
            preload: true,
            theme: false
        },
        config: {
            notice: false,
            cdn: cdn,
            api: api,
            webp: false,
            page: {
                page: 'index',
                active: 'index',
                adNum: 0,
                num: 0,
                size: 24,
                pageSize: 120,
                current: 1,
                pages: 0,
                flag4View: true,
                flag4Data: true
            },
            lazy: {
                preLoad: 2,
                attempt: 8,
                loading: 'img/zwt.png'
            },
            classify: {
                menu: '',
                menuMap: {
                    colors: []
                },
                params: {
                    sort: 0,
                    color: -1,
                    dimensionX: null,
                    dimensionY: null,
                    fileType: -1,
                    createAt: -1,
                    category: -1
                },
                values: {
                    sort: '按推荐',
                    color: '不限',
                    dimension: '不限',
                    fileType: '不限',
                    createAt: '不限',
                    category: '不限'
                }
            },
            comment: {
                page: 10
            },
            modal: '',
            text_message: '',
            danger: false,
            loading: true
        },
        target: {
            index: -1,
            type: '',
            el: ''
        },
        full: {
            height: 0,
            width: 0,
            show: false,
            fullScreen: false,
            blur: 5,
            index: -1,
            loading: {
                show: false,
                per: 0
            }
        },
        message: {
            show: false,
            per: 0,
            type: '',
            text: '',
            time: 2000,
            timeout: null
        },
        user: {
            isLogin: false,
            login: {
                username: '',
                password: ''
            },
            register: {
                username: '',
                password: '',
                password2: '',
                email: ''
            },
            userinfo: {
                username: '',
                token: '',
                cloudCount: 0,
                localCount: 0
            }
        }
    },
    methods: {
        Alert: function Alert(text, type, time) {
            clearTimeout(this.message.timeout);
            this.message.text = typeof text == 'string' && text ? text: '请稍后...';
            this.message.type = 'c-message--' + (type ? type: 'info');
            this.message.time = time ? time: 2000;
            this.message.show = true;
            if (this.message.text == 'download') {
                this.message.per = 0
            } else {
                this.message.timeout = setTimeout(function() {
                    vm.message.show = false
                },
                this.message.time)
            }
        },
        loadMoreComment: function loadMoreComment() {
            vm.config.comment.page += 10
        },
        hideLive2d: function hideLive2d() {
            var xxb = document.querySelector('#xuexiaoban');
            if (xxb != null) {
                xxb.style.opacity = '0';
                xxb.style.zIndex = '-1'
            }
        },
        encodeHtml: function encodeHtml(s) {
            return s.replace(/<(?!img).*?>/g, ' ... ')
        },
        loadComments: function loadComments() {
            this.ajax('post', this.config.api + 'sys/getCommentByType', JSON.stringify({
                type: 2
            }), 'json',
            function(r) {
                vm.json.comments = r.result
            },
            function() {
                vm.Alert('抱歉，服务器正在维护中，请稍后再试。', 'error', 5000)
            });
            if (localStorage.getItem('username')) {
                document.querySelector('#comment-name').value = localStorage.getItem('username')
            }
        },
        send: function send(type, name, message, contact) {
            this.Alert('发送中，请稍后', 'info', 10000);
            this.ajax('post', this.config.api + 'sys/submitComment', JSON.stringify({
                type: type,
                name: name == null ? null: this.encode(name),
                contact: contact == null ? contact: this.encode(contact),
                message: message == null ? message: this.encode(message.replace(new RegExp("<br>", "g"), "&nbsp;").replace(new RegExp("<br/>", "g"), "&nbsp;").replace(new RegExp("<div>", "g"), "&nbsp;").replace(new RegExp("</div>", "g"), "&nbsp;"))
            }), 'json',
            function(r) {
                if (r.code == 0) {
                    vm.Alert('发送成功', 'success', 5000);
                    if (type == 2) {
                        vm.loadComments();
                        document.querySelector('#comment-name').value = '';
                        document.querySelector('#comment-message').innerHTML = ''
                    } else if (type == 3) {
                        document.querySelector('#feedback-contact').value = '';
                        document.querySelector('#feedback-message').value = '';
                        vm.closeAll()
                    }
                } else {
                    vm.Alert('发送失败，服务器可能在维护中，请稍后再试', 'error', 5000)
                }
            },
            function(status) {
                vm.Alert('发送失败，服务器可能在维护中，请稍后再试', 'error', 5000)
            })
        },
        sendComment: function sendComment() {
            var name = document.querySelector('#comment-name');
            var message = document.querySelector('#comment-message');
            if (!name.value) {
                this.Alert('昵称不能为空', 'error', 5000);
                name.focus()
            } else if (!message.innerHTML) {
                this.Alert('评论的内容不能为空', 'error', 5000);
                message.focus()
            } else {
                this.send(2, name.value, message.innerHTML)
            }
        },
        sendFeedback: function sendFeedback() {
            var contact = document.querySelector('#feedback-contact');
            var message = document.querySelector('#feedback-message');
            if (!contact.value) {
                this.Alert('抱歉，联系方式不能为空', 'error', 5000);
                contact.focus()
            } else if (!message.value) {
                this.Alert('抱歉，意见反馈的内容不能为空', 'error', 5000);
                message.focus()
            } else {
                this.send(3, '壁纸意见反馈', message.value, contact.value)
            }
        },
        gotoComment: function gotoComment() {
            if (vm.config.page.active == 'about') {
                var y = document.querySelector('hr').offsetTop - 40;
                window.scrollTo(0, y);
                document.querySelector('#comment-name').focus()
            }
        },
        emoticon: function emoticon(i) {
            var emo = '<img src="img/emoticon/' + i + '.png" class="emoticon">';
            document.querySelector('#comment-message').innerHTML += emo
        },
        sign: function sign(callback) {
            var sign = sessionStorage.getItem("sign");
            if (sign) {
                callback(sign)
            } else {
                try {
                    Fingerprint2.get({
                        excludes: {
                            fonts: true,
                            fontsFlash: true,
                            audio: true,
                            enumerateDevices: true
                        }
                    },
                    function(components) {
                        sign = Fingerprint2.x64hash128(components.map(function(component) {
                            return component.value
                        }).join(''), 31);
                        sessionStorage.setItem("sign", sign);
                        callback(sign)
                    })
                } catch(e) {
                    callback('error')
                }
            }
        },
        ajax: function ajax(type, url, data, format, success, error, token) {
            var r = new XMLHttpRequest();
            r.open(type, url, true);
            r.timeout = 60000;
            this.sign(function(sign) {
                var timestamp = new Date().getTime();
                var location = window.location.host;
                var contentType = "application/json";
                var access = sha256(contentType + location + sign + timestamp);
                r.setRequestHeader("Sign", sign);
                r.setRequestHeader("Location", location);
                r.setRequestHeader("Content-Type", contentType);
                r.setRequestHeader("Timestamp", String(timestamp));
                r.setRequestHeader("Access", access);
                if (token) {
                    r.setRequestHeader("token", token)
                }
                r.send(data);
                r.onreadystatechange = function() {
                    if (r.readyState == 4) {
                        if (r.status == 200) {
                            if (success) {
                                if (format == 'json' || format == 'JSON') {
                                    success(JSON.parse(r.responseText))
                                } else {
                                    success(r.responseText)
                                }
                            }
                        } else {
                            if (error) {
                                error()
                            }
                        }
                    }
                }
            })
        },
        initColors: function initColors() {
            NProgress.start();
            this.ajax('post', this.config.api + 'bz/getColors', null, 'json',
            function(r) {
                if (r.code == 0) {
                    vm.config.classify.menuMap.colors = r.result;
                    NProgress.done()
                }
            },
            function() {
                setTimeout(function() {
                    vm.initColors()
                },
                20000)
            })
        },
        initData: function initData(num) {
            NProgress.start();
            this.config.page.current += num;
            var url, data, page;
            page = this.config.page.page;
            if (page == 'index' || page == 'people' || page == 'anime') {
                url = this.config.api + 'bz/getJson';
                data = JSON.stringify({
                    target: this.config.page.page,
                    pageNum: this.config.page.current
                })
            } else if (page == 'classify') {
                url = this.config.api + 'bz/getJsonByType';
                this.config.classify.params.target = this.config.page.page;
                this.config.classify.params.pageNum = this.config.page.current;
                data = JSON.stringify(this.config.classify.params)
            }
            if (this.json.data.length < this.config.page.current * this.config.page.pageSize && this.config.page.flag4Data) {
                this.config.page.flag4Data = false;
                this.ajax('post', url, data, 'json',
                function(r) {
                    if (r.code == 0) {
                        var _vm$json$data; (_vm$json$data = vm.json.data).push.apply(_vm$json$data, r.result.records);
                        vm.config.page.pageSize = r.result.size;
                        vm.config.page.current = r.result.current;
                        vm.config.page.pages = r.result.pages;
                        vm.initView(0);
                        vm.config.page.flag4Data = true;
                        NProgress.done()
                    } else {
                        vm.Alert('抱歉，服务器又开小差了，得等我再调教调教。', 'error', 30000);
                        vm.config.page.flag4Data = true;
                        setTimeout(function() {
                            vm.initData(num)
                        },
                        60000)
                    }
                },
                function() {
                    vm.Alert('抱歉，服务器又不好好干活了，请晚点再试下好了。', 'error', 30000);
                    vm.config.page.flag4Data = true;
                    setTimeout(function() {
                        vm.initData(num)
                    },
                    60000)
                })
            } else {
                NProgress.done()
            }
        },
        initView: function initView(num) {
            this.config.page.num += num;
            if (this.json.view.length < this.json.data.length && this.json.view.length < (this.config.page.num + 1) * this.config.page.size && this.config.page.flag4View) {
                var _this$json$view;
                this.config.page.flag4View = false; (_this$json$view = this.json.view).push.apply(_this$json$view, this.json.data.slice(this.config.page.num * this.config.page.size, (this.config.page.num + 1) * this.config.page.size));
                if (this.config.page.active != 'like' && this.config.page.num > 2 && this.config.page.num % 2 == 1) {
                    var adData = {
                        i: 'ad_' + this.config.page.adNum,
                        t: 'ad',
                        x: 0,
                        y: 0
                    };
                    this.config.page.adNum++;
                    this.json.view.push(adData)
                }
                this.config.page.flag4View = true
            } else if (this.json.view.length == (this.config.page.num + 1) * this.config.page.size) {
                this.initView(1)
            }
        },
        showClassifyMenu: function showClassifyMenu(menu) {
            this.config.classify.menu = menu
        },
        closeClassifyMenu: function closeClassifyMenu() {
            this.config.classify.menu = ''
        },
        changeClassifyMenu: function changeClassifyMenu(menu, value, color) {
            this.json.data = new Array();
            this.json.view = new Array();
            this.config.page.num = 0;
            this.config.page.current = 1;
            if (menu == 'reset') {
                this.config.classify.params = {
                    sort: 0,
                    color: -1,
                    dimensionX: null,
                    dimensionY: null,
                    fileType: -1,
                    createAt: -1,
                    category: -1
                };
                this.config.classify.values = {
                    sort: '按推荐',
                    color: '不限',
                    dimension: '不限',
                    fileType: '不限',
                    createAt: '不限',
                    category: '不限'
                }
            } else if (menu == 'category') {
                this.config.classify.params.category = value;
                switch (value) {
                case - 1 : {
                        this.config.classify.values.category = '不限';
                        break
                    }
                case 0:
                    {
                        this.config.classify.values.category = '精选';
                        break
                    }
                case 1:
                    {
                        this.config.classify.values.category = '人物';
                        break
                    }
                case 2:
                    {
                        this.config.classify.values.category = '二次元';
                        break
                    }
                }
            } else if (menu == 'fileType') {
                this.config.classify.params.fileType = value;
                switch (value) {
                case - 1 : {
                        this.config.classify.values.fileType = '不限';
                        break
                    }
                case 0:
                    {
                        this.config.classify.values.fileType = 'JPEG';
                        break
                    }
                case 1:
                    {
                        this.config.classify.values.fileType = 'PNG';
                        break
                    }
                }
            } else if (menu == 'sort') {
                this.config.classify.params.sort = value;
                switch (value) {
                case 0:
                    {
                        this.config.classify.values.sort = '按推荐';
                        break
                    }
                case 1:
                    {
                        this.config.classify.values.sort = '按最热';
                        break
                    }
                case 2:
                    {
                        this.config.classify.values.sort = '按最新';
                        break
                    }
                case 3:
                    {
                        this.config.classify.values.sort = '按分辨率';
                        break
                    }
                case 4:
                    {
                        this.config.classify.values.sort = '按文件大小';
                        break
                    }
                }
            } else if (menu == 'dimension') {
                switch (value) {
                case - 1 : {
                        this.config.classify.params.dimensionX = null;
                        this.config.classify.params.dimensionY = null;
                        break
                    }
                case 0:
                    {
                        this.config.classify.params.dimensionX = '1920';
                        this.config.classify.params.dimensionY = '1080';
                        break
                    }
                case 1:
                    {
                        this.config.classify.params.dimensionX = '2560';
                        this.config.classify.params.dimensionY = '1080';
                        break
                    }
                case 2:
                    {
                        this.config.classify.params.dimensionX = '3840';
                        this.config.classify.params.dimensionY = '2160';
                        break
                    }
                case 3:
                    {
                        this.config.classify.params.dimensionX = '7680';
                        this.config.classify.params.dimensionY = '4320';
                        break
                    }
                case 4:
                    {
                        if (!this.config.classify.params.dimensionX) this.config.classify.params.dimensionX = 0;
                        if (!this.config.classify.params.dimensionY) this.config.classify.params.dimensionY = 0;
                        break
                    }
                }
                this.config.classify.values.dimension = value == -1 ? '不限': this.config.classify.params.dimensionX + 'x' + this.config.classify.params.dimensionY
            } else if (menu == 'color') {
                this.config.classify.params.color = value;
                this.config.classify.values.color = color
            } else if (menu == 'createAt') {
                this.config.classify.params.createAt = value;
                switch (value) {
                case - 1 : {
                        this.config.classify.values.createAt = '不限';
                        break
                    }
                case 0:
                    {
                        this.config.classify.values.createAt = '1个月内';
                        break
                    }
                case 1:
                    {
                        this.config.classify.values.createAt = '3个月内';
                        break
                    }
                case 2:
                    {
                        this.config.classify.values.createAt = '6个月内';
                        break
                    }
                case 3:
                    {
                        this.config.classify.values.createAt = '1年以内';
                        break
                    }
                }
            }
            this.closeClassifyMenu();
            this.initData(0)
        },
        enct: function enct(id) {
            var a, b, c, e, t, f = [],
            j = 0,
            i = 0,
            g,
            r = '';
            var s = [104, 221, 19, 198, 11, 124, 71, 108, 81, 32, 110, 172, 21, 200, 55, 142, 36, 64, 103, 233, 84, 80, 94, 208, 49, 226, 79, 78, 60, 248, 214, 111, 212, 164, 53, 46, 48, 152, 44, 122, 93, 239, 77, 72, 230, 251, 22, 114, 204, 106, 146, 203, 115, 116, 17, 100, 202, 160, 23, 57, 69, 148, 70, 245, 121, 244, 101, 27, 125, 243, 168, 105, 242, 140, 217, 88, 210, 2, 161, 153, 194, 92, 219, 95, 126, 139, 192, 220, 91, 52, 182, 123, 252, 157, 196, 188, 83, 67, 209, 166, 162, 15, 120, 128, 42, 177, 159, 99, 38, 228, 29, 9, 144, 87, 141, 31, 18, 45, 130, 205, 195, 63, 37, 68, 134, 4, 132, 41, 40, 240, 183, 180, 178, 154, 89, 138, 34, 191, 149, 163, 238, 50, 74, 170, 249, 181, 218, 213, 62, 155, 117, 133, 75, 199, 179, 33, 223, 56, 254, 207, 107, 136, 185, 175, 12, 229, 102, 65, 187, 20, 73, 211, 113, 7, 109, 193, 137, 10, 184, 206, 171, 14, 76, 235, 250, 173, 35, 158, 119, 253, 66, 232, 54, 0, 222, 247, 28, 51, 151, 1, 156, 165, 246, 225, 145, 6, 131, 186, 61, 129, 234, 236, 190, 216, 26, 39, 58, 201, 90, 47, 174, 43, 8, 176, 86, 255, 237, 118, 24, 143, 112, 147, 189, 82, 96, 98, 150, 241, 16, 85, 167, 97, 215, 5, 169, 197, 13, 231, 135, 59, 25, 30, 3, 224, 227, 127];
            for (a = 0; a < id.length; a++) {
                c = id.charCodeAt(a);
                e = [];
                do {
                    e.push(c & 0xFF);
                    c = c >> 8
                } while ( c );
                f = f.concat(e.reverse())
            }
            b = new Array(f.length);
            for (a = 0; a < f.length; a++) {
                i = (i + 1) % 256;
                j = (j + s[i]) % 256;
                g = s[i];
                s[i] = s[j];
                s[j] = g;
                t = (s[i] + s[j]) % 256;
                b[a] = f[a] ^ s[t]
            }
            for (a = 0; a < b.length; a++) {
                g = b[a].toString(16);
                if (g.length == 1) {
                    g = "0" + g
                }
                r += g
            }
            return r
        },
        getUrl: function getUrl(i, t, f) {
            var url = "";
            if (f) {
                url = 'https://w.wallhaven.cc/full/' + i.substring(0, 2) + '/' + 'wallhaven-' + i + (t == 'j' ? '.jpg': '.png')
            } else {
                url = 'https://th.wallhaven.cc/small/' + i.substring(0, 2) + '/' + i + '.jpg'
            }
            return url
        },
        init: function init() {
            title();
            this.closeAll();
            window.scrollTo(0, 0);
            this.json.data = new Array();
            this.json.view = new Array();
            if (window.location.hash) {
                this.config.page.page = window.location.hash.replace('#', '');
                this.config.page.active = this.config.page.page
            }
            if (this.config.page.page) {
                if (this.config.page.page == 'index' || this.config.page.page == 'people' || this.config.page.page == 'anime') {
                    this.config.page.num = 0;
                    this.config.page.current = 1;
                    this.initData(0)
                } else if (this.config.page.page == 'classify') {
                    this.config.page.num = 0;
                    this.config.page.current = 1;
                    this.initColors();
                    this.initData(0)
                } else if (this.config.page.page == 'like') {
                    this.json.data = this.json.likes;
                    this.config.page.num = 0;
                    this.initView(0)
                } else if (this.config.page.page == 'about') {
                    this.loadComments();
                    this.load2djs()
                }
                if (this.config.page.page != 'about') {
                    this.hideLive2d()
                }
                loadAdsense(this.config.page.page)
            }
            window._hmt && window._hmt.push(['_trackEvent', 'page', 'init', this.config.page.page])
        },
        load2djs: function load2djs() {
            var live2d = document.querySelector('#live2djs');
            if (live2d) {
                loadxxb()
            } else {
                var script = document.createElement("script");
                script.id = 'live2djs';
                script.type = 'text/javascript';
                script.src = this.config.cdn + 'live2d/js/live2d.min.js';
                document.getElementsByTagName('body')[0].appendChild(script);
                script.onload = function() {
                    loadxxb()
                }
            }
        },
        showFull: function showFull(index) {
            if (this.settings.fullScreen) this.entryFullScreen();
            this.full.index = index;
            this.full.show = true;
            document.documentElement.style.overflowY = 'hidden';
            this.draw()
        },
        draw: function draw() {
            var data = this.json.view[this.full.index];
            var canvas = document.querySelector('canvas');
            var ctx = canvas.getContext('2d');
            var small = data && data.i ? document.getElementById(data.i) : null;
            this.full.height = data.y;
            this.full.width = data.x;
            if (small) {
                canvas.height = data.y;
                canvas.width = data.x;
                ctx.drawImage(small, 0, 0, data.x, data.y);
                canvas.style.filter = 'blur(' + this.full.blur + 'px)';
                var box = document.getElementById('box_' + data.i);
                if (box) {
                    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
                    var windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
                    var offsetTop = box.offsetTop;
                    var height = box.offsetHeight;
                    if (offsetTop + 40 >= scrollTop + windowHeight) {
                        window.scrollTo(0, offsetTop - windowHeight + height)
                    }
                }
            }
            this.full.loading.per = 0;
            this.full.loading.show = true;
            var url = this.getUrl(data.i, data.t, true);
            this.obj.imgXhr.open('get', url, true);
            this.obj.imgXhr.send(null);
            this.obj.imgXhr.onload = function(event) {
                var image = new Image();
                image.crossOrigin = 'Anonymous';
                image.onload = function() {
                    var canvas = document.querySelector('canvas');
                    var ctx = canvas.getContext('2d');
                    canvas.width = image.naturalWidth;
                    canvas.height = image.naturalHeight;
                    ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
                    vm.full.loading.show = false;
                    canvas.style.filter = 'none';
                    if (vm.settings.preload && vm.full.show && vm.full.index < vm.json.data.length - 1) {
                        var next = vm.json.view[parseInt(vm.full.index) + 1];
                        if (next && next.t && next.t != 'ad') {
                            var newXhr = new XMLHttpRequest();
                            newXhr.open('get', vm.getUrl(next.i, next.t, true), true);
                            newXhr.send(null)
                        }
                    }
                };
                image.src = url
            };
            this.obj.imgXhr.onprogress = function(event) {
                if (event.lengthComputable) {
                    vm.full.loading.per = Math.round(100 * event.loaded / event.total);
                    canvas.style.filter = 'blur(' + vm.full.blur * (1 - vm.full.loading.per / 100) + 'px)'
                }
            };
            window._hmt && window._hmt.push(['_trackEvent', 'image', 'showFull', data.i]);
            vm.ajax('post', vm.config.api + 'bz/bzCount', JSON.stringify({
                'id': data.i,
                'type': 0
            }), 'json')
        },
        download: function download(i) {
            this.Alert('download', 'info', 10000);
            var target = this.json.view[i];
            var id = target.i;
            var exn = target.t == 'j' ? 'jpg': 'png';
            var a = document.createElement('a');
            a.download = id + '.' + exn;
            var url = this.getUrl(id, target.t, true);
            this.obj.imgXhr.open('GET', url, true);
            this.obj.imgXhr.responseType = "blob";
            this.obj.imgXhr.onload = function() {
                var blob = this.response;
                if (typeof MouseEvent === 'function') {
                    a.href = window.URL.createObjectURL(blob);
                    var mouseEvent = new MouseEvent('click', {
                        view: window,
                        bubbles: false,
                        cancelable: false
                    });
                    a.dispatchEvent(mouseEvent)
                } else {
                    window.navigator.msSaveBlob(blob, id + '.' + exn)
                }
                vm.Alert('保存成功', 'success')
            };
            this.obj.imgXhr.onprogress = function(event) {
                if (event.lengthComputable) {
                    vm.message.per = Math.round(100 * event.loaded / event.total)
                }
            };
            this.obj.imgXhr.send(null);
            window._hmt && window._hmt.push(['_trackEvent', 'image', 'download', data.i]);
            vm.ajax('post', vm.config.api + 'bz/bzCount', JSON.stringify({
                'id': data.i,
                'type': 1
            }), 'json')
        },
        closeAll: function closeAll() {
            this.exitFullScreen();
            this.full.show = false;
            this.config.modal = '';
            this.config.notice = false;
            document.documentElement.style.overflowY = 'auto';
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'closeFullScreen'])
        },
        next: function next() {
            if (this.full.show && this.full.index / this.json.view.length >= 0.9) {
                vm.initView(1)
            }
            if (this.full.show && this.full.index < this.json.data.length - 1) {
                this.full.index++;
                var _data = this.json.view[this.full.index];
                if (_data && _data.t == 'ad') {
                    this.full.index++
                }
                this.draw()
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'next'])
        },
        prev: function prev() {
            if (this.full.show && this.full.index > 0) {
                this.full.index--;
                var _data2 = this.json.view[this.full.index];
                if (_data2 && _data2.t == 'ad') {
                    this.full.index--
                }
                this.draw()
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'prev'])
        },
        fullScreen: function fullScreen() {
            if (document.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement) {
                this.exitFullScreen()
            } else {
                this.entryFullScreen()
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'fullScreen'])
        },
        entryFullScreen: function entryFullScreen() {
            var element = document.documentElement;
            if (element.requestFullscreen) {
                element.requestFullscreen()
            } else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen()
            } else if (element.mozRequestFullScreen) {
                element.mozRequestFullScreen()
            } else if (element.msRequestFullscreen) {
                element.msRequestFullscreen()
            }
            this.full.fullScreen = true;
            this.Alert('已进入全屏', 'success')
        },
        exitFullScreen: function exitFullScreen() {
            if (document.fullScreen || document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement) {
                if (document.exitFullscreen) {
                    document.exitFullscreen()
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen()
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen()
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen()
                }
                this.full.fullScreen = false;
                this.Alert('已退出全屏', 'info')
            }
        },
        isLike: function isLike(i) {
            for (var index in this.json.likes) {
                var j = this.json.likes[index];
                if (this.json.view[i] && j.i == this.json.view[i].i) return true
            }
            return false
        },
        like: function like(i) {
            var data = this.json.view[i];
            var isLike = this.isLike(i);
            var classes = document.querySelector('#box_' + data.i + ' .like-span').classList;
            if (isLike) {
                classes.remove('iconheart-fill');
                classes.add('iconheart');
                this.removeLike(data);
                this.Alert('已取消喜欢', 'warning')
            } else {
                classes.remove('iconheart');
                classes.add('iconheart-fill');
                this.addLike(data);
                this.Alert('已添加到喜欢', 'success')
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'like'])
        },
        removeLike: function removeLike(data) {
            for (var i in this.json.likes) {
                if (this.json.likes[i].i == data.i) {
                    this.json.likes.splice(i, 1);
                    this.delOne(data)
                }
            }
            this.user.userinfo.cloudCount = this.json.likes.length;
            this.user.userinfo.localCount = this.json.likes.length;
            vm.ajax('post', vm.config.api + 'bz/bzCount', JSON.stringify({
                'id': data.i,
                'type': 3
            }), 'json')
        },
        addLike: function addLike(data) {
            if (this.user.userinfo.localCount >= 1000) {
                this.Alert('', '', '');
                return false
            }
            for (var index in this.json.likes) {
                var temp = this.json.likes[index];
                if (temp.i == data.i) return
            }
            this.json.likes.unshift(data);
            this.putOne(data);
            this.user.userinfo.cloudCount = this.json.likes.length;
            this.user.userinfo.localCount = this.json.likes.length;
            window._hmt && window._hmt.push(['_trackEvent', 'image', 'like', data.i]);
            vm.ajax('post', vm.config.api + 'bz/bzCount', JSON.stringify({
                'id': data.i,
                'type': 2
            }), 'json')
        },
        modal: function modal(target) {
            this.config.modal = target;
            if (target == 'prizesList') {
                this.ajax('post', this.config.api + 'bz/getPrizesList', null, 'json',
                function(r) {
                    if (r.code == 0) {
                        vm.json.prizesList = r.result
                    } else {
                        vm.Alert('服务器维护中，请稍后再试', 'error', 5000)
                    }
                })
            } else if (target == 'login') {
                this.config.text_message = '已有账号的用户请在此登录';
                this.config.danger = false
            } else if (target == 'register') {
                this.config.text_message = '极简壁纸 欢迎您注册成为新会员';
                this.config.danger = false
            }
        },
        register: function register() {
            var emailRegExp = /^([a-z0-9A-Z]+[-|\.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\.)+[a-zA-Z]{2,}$/;
            var nameRegExp = /^[a-zA-Z0-9\u4e00-\u9fa5]{1,10}$/;
            var pwdRegExp = /^[a-zA-Z0-9]{6,32}$/;
            if (!nameRegExp.test(this.user.register.username)) {
                this.config.danger = true;
                this.config.text_message = '用户名不正确，推荐使用[汉字/字母/数字]，不超过10个字';
                this.Alert('用户名不正确', 'error', 5000)
            } else if (this.user.register.password != this.user.register.password2) {
                this.config.danger = true;
                this.config.text_message = '两次密码输入不一致';
                this.Alert('两次密码输入不一致', 'error', 5000)
            } else if (!pwdRegExp.test(this.user.register.password)) {
                this.config.danger = true;
                this.config.text_message = '密码格式不正确，至少超过6位，可以是字母数字的组合';
                this.Alert('密码不正确', 'error', 5000)
            } else if (!emailRegExp.test(this.user.register.email)) {
                this.config.danger = true;
                this.config.text_message = '邮箱格式不正确，请填写正确的邮箱';
                this.Alert('邮箱不正确', 'error', 5000)
            } else {
                this.Alert('注册中...', 'info', 5000);
                this.ajax('post', this.config.api + 'bz/user/registerBzUser', JSON.stringify({
                    'username': vm.user.register.username,
                    'password': vm.user.register.password,
                    'email': vm.user.register.email
                }), 'json',
                function(result) {
                    if (result.code == 0) {
                        vm.Alert('注册成功，请登录', 'success', 5000);
                        vm.user.login.username = vm.user.register.username;
                        vm.modal('login')
                    } else {
                        vm.config.danger = true;
                        vm.config.text_message = result.msg;
                        vm.Alert(result.msg, 'error', 5000)
                    }
                },
                function(status) {
                    vm.config.danger = true;
                    vm.config.text_message = '服务器维护中，请稍后再试';
                    vm.Alert('服务器维护中，请稍后再试。', 'error', 5000)
                })
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'register'])
        },
        login: function login() {
            if (!this.user.login.username || !this.user.login.password) {
                this.config.text_message = '用户名或密码不能为空';
                this.config.danger = true;
                return
            }
            var data = JSON.stringify({
                'username': this.user.login.username,
                'password': this.user.login.password
            });
            this.ajax('post', this.config.api + 'bz/user/loginBzUser', data, 'json',
            function(result) {
                vm.config.danger = true;
                if (result.code == 0) {
                    vm.config.text_message = '登录成功';
                    var name = result.result.username;
                    vm.Alert('登录成功 欢迎你!', 'success', 5000);
                    localStorage.setItem("token", result.result.token);
                    localStorage.setItem("username", name);
                    vm.user.userinfo.username = name;
                    vm.user.isLogin = true;
                    vm.closeAll();
                    vm.initLogin()
                } else if (result.code == 401) {
                    vm.config.text_message = '您的输入有误，请重新输入';
                    vm.Alert('您的输入有误，请重新输入', 'error', 5000)
                } else if (result.code == 605) {
                    vm.config.text_message = '用户名或密码错误 （若还没有账号请先注册）';
                    vm.Alert('用户名或密码错误', 'error', 5000)
                } else {
                    vm.config.text_message = '服务器维护中，请稍后再试';
                    vm.Alert('服务器维护中，请稍后再试', 'error', 5000)
                }
            },
            function(status) {
                this.config.text_message = '服务器维护中，请稍后再试';
                vm.Alert('服务器维护中，请稍后再试。', 'error', 5000)
            });
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'login'])
        },
        logout: function logout(showMsg) {
            localStorage.removeItem('username');
            localStorage.removeItem('token');
            localStorage.removeItem('uploaded');
            sessionStorage.removeItem('downloaded');
            this.config.text_message = '已有账号的用户请在此登录';
            this.config.danger = false;
            this.user.isLogin = false;
            this.user.userinfo.username = '';
            this.user.userinfo.token = '';
            if (showMsg) {
                vm.Alert('已注销登录', 'error', 5000);
                this.closeAll()
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'logout'])
        },
        forceAsyncData: function forceAsyncData() {
            vm.Alert('同步中', 'info', 5000);
            var token = localStorage.getItem("token");
            if (token) {
                this.getJson(token, new Array(),
                function() {
                    vm.Alert('同步成功', 'success', 1000)
                })
            }
            window._hmt && window._hmt.push(['_trackEvent', 'button', 'click', 'forceAsyncData'])
        },
        initLogin: function initLogin() {
            var username = localStorage.getItem("username");
            var token = localStorage.getItem("token");
            if (token && username) {
                this.user.isLogin = true;
                this.user.userinfo.token = token;
                this.user.userinfo.username = username;
                var array = localStorage.getItem("firstLogin") != "true" ? this.uniqueJson(this.json.likes) : new Array();
                this.getJson(token, array,
                function() {
                    vm.Alert('同步成功', 'success', 1000);
                    localStorage.setItem("firstLogin", "true")
                })
            }
        },
        getJson: function getJson(token, data, method) {
            this.ajax('post', this.config.api + 'bz/user/getJson', JSON.stringify(data), 'json',
            function(result) {
                if (result && result.code == 0 && result.result && result.result.json) {
                    sessionStorage.setItem('downloaded', '1');
                    var likes = result.result.json ? result.result.json: JSON.parse('[]');
                    var size = result.result.size ? result.result.size: 0;
                    var localJson = JSON.parse(localStorage.getItem('wallpaper_v3') ? localStorage.getItem('wallpaper_v3') : '[]');
                    localStorage.setItem('wallpaper_v3', JSON.stringify(vm.uniqueJson(localJson)));
                    vm.user.userinfo.cloudCount = size;
                    vm.user.userinfo.localCount = localJson.length;
                    vm.json.likes = vm.uniqueJson(likes);
                    vm.user.userinfo.localCount = likes.length;
                    if (vm.config.page.page == 'like') {
                        vm.json.view = new Array();
                        vm.json.data = vm.json.likes;
                        vm.initView(0)
                    }
                    if (method) method()
                } else if (result.code == 600 || result.code == 601) {
                    vm.logout()
                }
            },
            function() {},
            token)
        },
        delOne: function delOne(obj) {
            var token = localStorage.getItem("token");
            if (token) {
                this.ajax('post', this.config.api + 'bz/user/delete', JSON.stringify(obj), 'json',
                function(result) {},
                function(status) {},
                token)
            }
        },
        putOne: function putOne(obj) {
            var token = localStorage.getItem("token");
            if (token) {
                this.ajax('post', this.config.api + 'bz/user/put', JSON.stringify(obj), 'json',
                function(result) {},
                function(status) {},
                token)
            }
        },
        uniqueJson: function uniqueJson(arr) {
            var new_arr = [];
            var result_arr = [];
            for (var i = 0; i < arr.length; i++) {
                if (new_arr.indexOf(arr[i].i) == -1) {
                    new_arr.push(arr[i].i);
                    result_arr.push(arr[i])
                }
            }
            return arr
        },
        encode: function encode(input) {
            var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
            var chr1, chr2, chr3, enc1, enc2, enc3, enc4, i = 0,
            output = '',
            utftext = '';
            input = input.replace(/\r\n/g, "\n");
            for (var n = 0; n < input.length; n++) {
                var c = input.charCodeAt(n);
                if (c < 128) {
                    utftext += String.fromCharCode(c)
                } else if (c > 127 && c < 2048) {
                    utftext += String.fromCharCode(c >> 6 | 192);
                    utftext += String.fromCharCode(c & 63 | 128)
                } else {
                    utftext += String.fromCharCode(c >> 12 | 224);
                    utftext += String.fromCharCode(c >> 6 & 63 | 128);
                    utftext += String.fromCharCode(c & 63 | 128)
                }
            }
            while (i < utftext.length) {
                chr1 = utftext.charCodeAt(i++);
                chr2 = utftext.charCodeAt(i++);
                chr3 = utftext.charCodeAt(i++);
                enc1 = chr1 >> 2;
                enc2 = (chr1 & 3) << 4 | chr2 >> 4;
                enc3 = (chr2 & 15) << 2 | chr3 >> 6;
                enc4 = chr3 & 63;
                if (isNaN(chr2)) {
                    enc3 = enc4 = 64
                } else if (isNaN(chr3)) {
                    enc4 = 64
                }
                output = output + _keyStr.charAt(enc1) + _keyStr.charAt(enc2) + _keyStr.charAt(enc3) + _keyStr.charAt(enc4)
            }
            return output
        },
        dateFormat: function dateFormat(timestamp, type) {
            var now = new Date(timestamp),
            y = now.getFullYear(),
            m = now.getMonth() + 1,
            d = now.getDate();
            var result = y + "-" + (m < 10 ? "0" + m: m) + "-" + (d < 10 ? "0" + d: d);
            if (!type) {
                result += " " + now.toTimeString().substr(0, 8)
            }
            return result
        },
        webp: function webp(callback) {
            var image = new Image();
            image.onerror = function() {
                return callback(false)
            };
            image.onload = function() {
                return callback(image.width > 0)
            };
            image.src = 'data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA='
        }
    },
    watch: {
        settings: {
            handler: function handler(newValue, oldValue) {
                localStorage.setItem('settings', JSON.stringify(newValue))
            },
            deep: true
        },
        'json.likes': {
            handler: function handler(newValue, oldValue) {
                localStorage.setItem('wallpaper_v3', JSON.stringify(newValue))
            },
            deep: true
        }
    },
    created: function created() {
        document.getElementById('bannerDiv').style.display = 'none';
        console.log("%c喂喂喂~\n是妖妖灵吗？\n就是这个人偷看控制台！\n快去抓住他！", "color:red");
        NProgress.configure({
            easing: 'ease',
            speed: 500,
            showSpinner: false
        });
        Vue.use(VueLazyload, {
            preLoad: this.config.lazy.preLoad,
            loading: this.config.lazy.loading,
            attempt: this.config.lazy.attempt,
            adapter: {
                loaded: function loaded(_ref) {
                    var bindType = _ref.bindType,
                    el = _ref.el,
                    naturalHeight = _ref.naturalHeight,
                    naturalWidth = _ref.naturalWidth,
                    $parent = _ref.$parent,
                    src = _ref.src,
                    loading = _ref.loading,
                    error = _ref.error,
                    Init = _ref.Init;
                    setTimeout(function() {
                        if (el.id && document.getElementById('box_' + el.id)) {
                            document.getElementById('box_' + el.id).style.filter = "none"
                        }
                    },
                    150);
                    var id = el.id;
                    var index = el.getAttribute('data-index');
                    var j = vm.json.view[index];
                    var target = document.getElementById('box_' + id);
                    if (id && index > -1 && target) {
                        var c = target.childNodes;
                        for (var i = 0; i < c.length; i++) {
                            var name = c[i].className;
                            if (name && (name.search(/res-span/i) > -1 || name.search(/down-span/i) > -1 || name.search(/like-span/i) > -1)) {
                                target.removeChild(c[i])
                            }
                        }
                        var heart = 'iconheart';
                        for (var _index in vm.json.likes) {
                            var l = vm.json.likes[_index];
                            if (l.i == id) {
                                heart = 'iconheart-fill';
                                break
                            }
                        }
                        if (j) {
                            var resSpan = document.createElement("span");
                            resSpan.className = 'res-span';
                            resSpan.innerHTML = j.x + 'x' + j.y;
                            target.appendChild(resSpan)
                        }
                        var downSpan = document.createElement("span");
                        downSpan.className = 'down-span';
                        downSpan.innerHTML = '保存';
                        downSpan.onclick = function() {
                            vm.download(index)
                        };
                        target.appendChild(downSpan);
                        var likeSpan = document.createElement("span");
                        likeSpan.className = 'like-span heart iconfont ' + heart;
                        likeSpan.onclick = function() {
                            vm.like(index)
                        };
                        target.appendChild(likeSpan)
                    }
                },
                loading: function loading(listender, Init) {
                    if (listender.el.id && document.getElementById('box_' + listender.el.id)) {
                        document.getElementById('box_' + listender.el.id).style.filter = "blur(3px)"
                    }
                },
                error: function error(listender, Init) {
                    if (listender.el.id && document.getElementById('box_' + listender.el.id)) document.getElementById('box_' + listender.el.id).style.display = 'none'
                }
            }
        });
        window.onkeydown = function(e) {
            var event = e || window.event;
            var code = event.which || event.keyCode;
            if (code >= 121 && code <= 123 || event.ctrlKey && event.shiftKey && code == 73) {
                return false
            } else if (vm.full.show && code == 83 && (event.ctrlKey || event.metaKey)) {
                event.preventDefault();
                vm.download(vm.full.index)
            } else if (vm.full.show) {
                switch (code) {
                case 37:
                case 65:
                    vm.prev();
                    break;
                case 38:
                case 87:
                    vm.fullScreen();
                    break;
                case 39:
                case 68:
                    vm.next();
                    break;
                case 40:
                case 83:
                    vm.download(vm.full.index);
                    break;
                case 32:
                    vm.like(vm.full.index);
                    break
                }
            } else if (code == 27) {
                vm.closeAll()
            }
        };
        window.oncontextmenu = function(ev) {
            var e = ev || event,
            menu;
            ev.preventDefault();
            var nodes = document.querySelectorAll('.mouse-right');
            nodes.forEach(function(node) {
                node.style.display = 'none'
            });
            if (e.target && e.target.getAttribute('data-type') == 'img-box') {
                menu = document.querySelector('.img-box-menu')
            } else if (e.target && e.target.getAttribute('data-type') == 'img-full') {
                menu = document.querySelector('.img-full-menu')
            } else if (e.target && e.target.id == 'live2d') {
                menu = document.querySelector('.xxb-menu')
            } else if (e.target && e.target.className != undefined && e.target.className.search(/modal/i) == -1 && e.target.className.search(/view-full/i) == -1) {
                menu = document.querySelector('.normal-menu')
            } else {
                return false
            }
            var clientWidth = document.documentElement.clientWidth;
            var clientHeight = document.documentElement.clientHeight;
            if (clientHeight - e.pageY >= menu.offsetHeight) {
                menu.style.top = e.pageY + 'px'
            } else {
                menu.style.top = e.pageY - menu.offsetHeight + 'px'
            }
            if (clientWidth - e.pageX >= menu.offsetWidth) {
                menu.style.left = e.pageX + 'px'
            } else {
                menu.style.left = e.pageX - menu.offsetWidth + 'px'
            }
            vm.target.index = e.target.getAttribute('data-index');
            vm.target.type = e.target.getAttribute('data-type');
            menu.style.display = 'block';
            window.onclick = function() {
                var nodes = document.querySelectorAll('.mouse-right');
                nodes.forEach(function(node) {
                    node.style.display = 'none'
                })
            }
        };
        window.onhashchange = function() {
            vm.init()
        };
        window.onscroll = function() {
            if (vm.config.page.active != 'about') {
                var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
                var windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
                var scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
                if (scrollTop + windowHeight >= scrollHeight - windowHeight) {
                    if ((vm.config.page.page == 'index' || vm.config.page.page == 'people' || vm.config.page.page == 'anime' || vm.config.page.page == 'classify') && vm.config.page.size * (vm.config.page.num + 2) >= vm.json.data.length) {
                        vm.initData(1)
                    } else {
                        vm.initView(1)
                    }
                }
            }
        }
    },
    mounted: function mounted() {
        if (localStorage.getItem('settings')) this.settings = JSON.parse(localStorage.getItem('settings'));
        else this.settings = this.default_settings;
        this.json.likes = localStorage.getItem('wallpaper_v3') ? JSON.parse(localStorage.getItem('wallpaper_v3')) : [];
        this.initLogin();
        this.webp(function(webp) {
            vm.config.webp = webp;
            vm.init();
            vm.config.loading = false;
            vm.config.notice = true
        })
    }
});