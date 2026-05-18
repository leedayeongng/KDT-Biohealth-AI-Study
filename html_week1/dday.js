<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>기념일</title>
    <script>
        // input  : 문자열(YYYY-MM-DD),숫자(100)
        // output : 문자열(YYYY-MM-DD)
        //특정 날짜로 부터 N일 뒤가 며칠인지 계산
        function fn_dday(start,days){
            let startDay = new Date(start);
            let startTime=startDay.getTime();
            let d_day = startTime + (days*(24*60*60*1000));
            let d_date = new Date(d_day);
            console.log(d_date);
            let year = d_date.getFullYear();
            let month = String(d_date.getMonth() + 1).padStart(2,'0');
            let day = String(d_date.getDate()).padStart(2,'0'); 
            // ` <-- 백틱 템플릿 리터럴
            // `${변수} 문자열`            
            return `${year}-${month}-${day}`;
        }
        let start = prompt("기념일 시작!", "2025-12-29");
        document.write(`${start} 기념일 시작! <br><br>`);
        for(let i = 100; i <= 1000; i+=100){
            document.write(`${i}일 ${fn_dday(start,i)}<br>`);
        }
        
    </script>
</head>
<body>
    
</body>
</html>