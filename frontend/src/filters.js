// %Y-%m-%dT%H:%M:%s:%ms+JST 形式を %Y/%m/%d %H:%M に変換するフィルタ
export function formatDateTime (value) {
    const formatDate = (date) => `${date[0]}/${date[1]}/${date[2]}`
    const formatTime = (time) => time.slice(0,5)
    
    let [date, time] = value.split('T')
    date = formatDate(date.split('-'))

    if (time) {
        time = formatTime(time)
        return `${date} ${time}`
    } else {
        return `${date}`
    }
}


// todo 引数に取った数値をカンマ区切りで返すフィルタ
export function commaSep(value) {
    if (typeof(value) === 'string') {
        return parseInt(value).toLocaleString()
    } else {
        return value.toLocaleString()
    }
}