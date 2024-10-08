/*!
 * dyCalendar is a JavaScript library for creating Calendar.
 *
 * Author: Yusuf Shakeel
 * https://github.com/yusufshakeel
 *
 * GitHub Link: https://github.com/yusufshakeel/dyCalendarJS
 *
 * MIT license
 * Copyright (c) 2016 Yusuf Shakeel
 *
 * Date: 2014-08-17 sunday
 */
/*! dyCalendarJS | (c) 2016 Yusuf Shakeel | https://github.com/yusufshakeel/dyCalendarJS */

(function (global) 
{

    "use strict";

    var
        //this will be used by the user.
        dycalendar = {},

        //window document
        document = global.document,

        //starting year
        START_YEAR = 1900,

        //end year
        END_YEAR = 9999,

        //name of the months
        monthName = {
            full: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            mmm: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },

        //name of the days
        dayName = {
            full: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            d: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
            dd: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
            ddd: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        };

    /**
     * this function will create month table.
     *
     * @param object data   this contains the calendar data
     * @param object option this is the settings object
     * @return html
     */
    function createMonthTable(data, option) 
    {
        var
            table, tr, td,
            r, c, count;

        table = document.createElement("table");
        tr = document.createElement("tr");
        //create 1st row for the day letters
        for (c = 0; c <= 6; c = c + 1) 
        {
            td = document.createElement("td");
            td.innerHTML = "SMTWTFS"[c];
            tr.appendChild(td);
        }
        table.appendChild(tr);

        //create 2nd row for dates
        tr = document.createElement("tr");

        //blank td
        for (c = 0; c <= 6; c = c + 1) 
        {
            if (c === data.firstDayIndex)
                break;
            td = document.createElement("td");
            td.setAttribute("class", "dycalender-blank-data");
            tr.appendChild(td);
        }

        //remaing td of dates for the 2nd row
        count = 1;
        while (c <= 6) 
        {
            td = document.createElement("td");
            td.setAttribute("id", count);
            td.setAttribute("class", "dst-date-user");
            td.innerHTML = count;
            if (option.date === count && option.month === data.today.monthIndex && option.highlighttargetdate === true)
                td.setAttribute("class", "dst-date-user dycalendar-target-date");
            tr.appendChild(td);
            count = count + 1;
            c = c + 1;
        }
        table.appendChild(tr);

        //create remaining rows
        for (r = 3; r <= 7; r = r + 1) 
        {
            tr = document.createElement("tr");
            for (c = 0; c <= 6; c = c + 1) 
            {
                if (count > data.totaldays) 
                {
                    table.appendChild(tr);
                    return table;
                }
                td = document.createElement('td');
                td.setAttribute("id", count);
                td.setAttribute("class", "dst-date-user");
                td.innerHTML = count;
                if (option.date === count && option.month === data.today.monthIndex && option.highlighttargetdate === true)
                    td.setAttribute("class", "dst-date-user dycalendar-target-date");
                //option.month
                count = count + 1;
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }

        return table;
    }

    /**
     * this function will draw Calendar Month Table
     *
     * @param object data   this contains the calendar data
     * @param object option this is the settings object
     * @return html
     */
    function drawCalendarMonthTable(data, option) 
    {

        var
            table,
            div, container, elem;

        //get table
        table = createMonthTable(data, option);

        //calendar container
        container = document.createElement("div");
        container.setAttribute("class", "dycalendar-month-container");

        //-------------------------- Header ------------------

        //header div
        div = document.createElement("div");
        div.setAttribute("class", "dycalendar-header");
        div.setAttribute("data-option", JSON.stringify(option));

        //prev button
        elem = document.createElement("span");
        elem.setAttribute("class", "dycalendar-prev-next-btn prev-btn");
        elem.setAttribute("id", "dycalendar-prev-next-btn");
        elem.setAttribute("data-date", option.date);
        elem.setAttribute("data-month", option.month);
        elem.setAttribute("data-year", option.year);
        elem.setAttribute("data-btn", "prev");
        elem.innerHTML = "&lt;";
        //add prev button span to header div
        div.appendChild(elem);

        //month span
        elem = document.createElement("span");
        elem.setAttribute("class", "dycalendar-span-month-year");
        if (option.monthformat === "mmm")
            elem.innerHTML = data.monthName + " " + data.year;
        else if (option.monthformat === "full")
            elem.innerHTML = data.monthNameFull + " " + data.year;

        //add month span to header div
        div.appendChild(elem);

        //next button
        elem = document.createElement("span");
        elem.setAttribute("class", "dycalendar-prev-next-btn next-btn");
        elem.setAttribute("data-date", option.date);
        elem.setAttribute("data-month", option.month);
        elem.setAttribute("data-year", option.year);
        elem.setAttribute("data-btn", "next");
        elem.innerHTML = "&gt;";
        //add prev button span to header div
        div.appendChild(elem);

        //add header div to container
        container.appendChild(div);

        //-------------------------- Body ------------------

        //body div
        div = document.createElement("div");
        div.setAttribute("class", "dycalendar-body");
        div.appendChild(table);

        //add body div to container div
        container.appendChild(div);

        //return container
        return container;
    }

    /**
     * This function will return calendar detail.
     *
     * @param integer year        1900-9999 (optional) if not set will consider
     *                          the current year.
     * @param integer month        0-11 (optional) 0 = Jan, 1 = Feb, ... 11 = Dec,
     *                          if not set will consider the current month.
     * @param integer date      1-31 (optional)
     * @return boolean|object    if error return false, else calendar detail
     */
    function getCalendar(year, month, date) 
    {

        var
            dateObj = new Date(),
            dateString,
            result = {},
            idx;

        if (year < START_YEAR || year > END_YEAR) 
        {
            global.console.error("Invalid Year");
            return false;
        }
        if (month > 11 || month < 0) 
        {
            global.console.error("Invalid Month");
            return false;
        }
        if (date > 31 || date < 1) 
        {
            global.console.error("Invalid Date");
            return false;
        }

        result.year = year;
        result.month = month;
        result.date = date;

        //today
        result.today = {};
        dateString = dateObj.toString().split(" ");

        idx = dayName.ddd.indexOf(dateString[0]);
        result.today.dayIndex = idx;
        result.today.dayName = dateString[0];
        result.today.dayFullName = dayName.full[idx];

        idx = monthName.mmm.indexOf(dateString[1]);
        result.today.monthIndex = idx;
        result.today.monthName = dateString[1];
        result.today.monthNameFull = monthName.full[idx];

        result.today.date = dateObj.getDate();

        result.today.year = dateString[3];

        //get month-year first day
        dateObj.setDate(1);
        dateObj.setMonth(month);
        dateObj.setFullYear(year);
        dateString = dateObj.toString().split(" ");

        idx = dayName.ddd.indexOf(dateString[0]);
        result.firstDayIndex = idx;
        result.firstDayName = dateString[0];
        result.firstDayFullName = dayName.full[idx];

        idx = monthName.mmm.indexOf(dateString[1]);
        result.monthIndex = idx;
        result.monthName = dateString[1];
        result.monthNameFull = monthName.full[idx];

        //get total days for the month-year
        dateObj.setFullYear(year);
        dateObj.setMonth(month + 1);
        dateObj.setDate(0);
        result.totaldays = dateObj.getDate();

        //get month-year targeted date
        dateObj.setFullYear(year);
        dateObj.setMonth(month);
        dateObj.setDate(date);
        dateString = dateObj.toString().split(" ");

        idx = dayName.ddd.indexOf(dateString[0]);
        result.targetedDayIndex = idx;
        result.targetedDayName = dateString[0];
        result.targetedDayFullName = dayName.full[idx];

        return result;

    }

    /**
     * this function will handle the on click event.
     */
    function onClick() 
    {

        document.body.onclick = function (e) 
        {

            //get event object (window.event for IE compatibility)
            e = global.event || e;

            var
                //get target dom object reference
                targetDomObject = e.target || e.srcElement,

                //other variables
                date, month, year, btn, last, option, dateObj;

            //prev-next button click
            //extra checks to make sure object exists and contains the class of interest
            if (targetDomObject && targetDomObject.classList)
            {
                if (targetDomObject.classList.contains("dycalendar-prev-next-btn")) 
                {
                    date = parseInt(targetDomObject.getAttribute("data-date"));
                    month = parseInt(targetDomObject.getAttribute("data-month"));
                    year = parseInt(targetDomObject.getAttribute("data-year"));
                    btn = targetDomObject.getAttribute("data-btn");
                    option = JSON.parse(targetDomObject.parentElement.getAttribute("data-option"));

                    if (btn === "prev") 
                    {
                        month = month - 1;
                        if (month < 0) 
                        {
                            year = year - 1;
                            month = 11;
                        }
                    }
                    else if (btn === "next") 
                    {
                        month = month + 1;
                        if (month > 11) 
                        {
                            year = year + 1;
                            month = 0;
                        }
                    }

                    option.date = date;
                    option.month = month;
                    option.year = year;

                    drawCalendar(option);
                }

                //month click
                //extra checks to make sure object exists and contains the class of interest
                if (targetDomObject.classList.contains("dycalendar-span-month-year")) 
                {
                    option = JSON.parse(targetDomObject.parentElement.getAttribute("data-option"));
                    dateObj = new Date();

                    option.date = dateObj.getDate();
                    option.month = dateObj.getMonth();
                    option.year = dateObj.getFullYear();

                    drawCalendar(option);
                }

                if (targetDomObject.classList.contains("dst-date-user")) 
                {

                    var
                        target = document.getElementById("dycalendar-prev-next-btn"),

                        data = {
                            year: target.getAttribute("data-year"),
                            month: target.getAttribute("data-month"),
                            date: parseInt(targetDomObject.getAttribute("id"))
                        }

                    createAppointedUser(data);
                }

                if (targetDomObject.classList.contains("dst-user-appointed")) 
                {

                    //对用户点击更新做出相应

                    updateAppointedUser(option);
                }
            }
        };
    }

    //------------------------------ dycalendar.draw() ----------------------

    /**
     * this function will draw the calendar based on user preferences.
     *
     * option = {
     *  target : "#id|.class"   //(mandatory) for id use #id | for class use .class
     *  type : "calendar-type"  //(optional) values: "day|month" (default "day")
     *  month : "integer"       //(optional) value 0-11, where 0 = January, ... 11 = December (default current month)
     *  year : "integer"        //(optional) example 1990. (default current year)
     *  date : "integer"        //(optional) example 1-31. (default current date)
     *  monthformat : "full"    //(optional) values: "mmm|full" (default "full")
     *  dayformat : "full"      //(optional) values: "ddd|full" (default "full")
     *  highlighttoday : boolean    //(optional) (default false) if true will highlight today's date
     *  highlighttargetdate : boolean   //(optional) (default false) if true will highlight targeted date of the month year
     *  prevnextbutton : "hide"         //(optional) (default "hide") (values: "show|hide") if set to "show" it will show the nav button (prev|next)
     * }
     *
     * @param object option     user preferences
     * @return boolean          true if success, false otherwise
     */
    dycalendar.draw = function () {

        var
            self = this,    //pointing at dycalendar object

            dateObj = new Date(),

            //default settings
            option = {
                year: dateObj.getFullYear(),
                month: dateObj.getMonth(),
                date: dateObj.getDate(),
                target: '#dycalendar',
                monthformat: "full",
                dayformat: "full",
                highlighttargetdate: true
            };

        drawCalendar(option);

        createAppointedUser(option);

    };

    //------------------------------ dycalendar.draw() ends here ------------

    /**
     * this function will draw the calendar inside the target container.
     */
    function drawCalendar(option) {

        var
            //variables for creating calendar
            calendar,
            calendarHTML,
            targetElem

        //find target element by
        targetElem = option.target.substring(1);

        //get calendar HTML
        //get calendar detail
        calendar = getCalendar(option.year, option.month, option.date);
        //get calendar html
        calendarHTML = drawCalendarMonthTable(calendar, option);

        //draw calendar
        document.getElementById(targetElem).innerHTML = calendarHTML.outerHTML;

    }

    // option{
    //    year,
    //    month，from 0 to 11
    //    date,
    //    ......
    //}
    function getData(option) {
        var 
            dateObj = new Date(),
            
            data 

        if (option.date === dateObj.getDate())
        {   
            data = [
                {
                    name: "xiaoming",
                    id: 210,
                    appointtype: 1,
                    appointtime: 15,
                    appointed: true
                },
                {
                    name: "xiaoming",
                    id: 210,
                    appointtype: 1,
                    appointtime: 13,
                    appointed: true
                },
                {
                    name: "xiaoming",
                    id: 210,
                    appointtype: 1,
                    appointtime: 12,
                    appointed: true
                }
            ]
        } 
        else
        {
            data = [
                {
                    name: "xiaoming",
                    id: 210,
                    appointtype: 1,
                    appointtime: 15,
                    appointed: true
                },
                {
                    name: "xiaoming",
                    id: 210,
                    appointtype: 1,
                    appointtime: 13,
                    appointed: true
                }
            ]
        }
        return data;
    }

    function updateAppointedUser(option)
    {

    }

    function createAppointedUser(option) 
    {
        var
            i, ul, li, user, all,
            property, count, data,
            length, end = "appoint-all",
            target =  "dyappoint-user"

        //传递数据
        data = getData(option);
        length = data.length;

        user = document.createElement("div");

        for (i = 0, count = 0; i < length; i = i + 1) 
        {
            ul = document.createElement("ul");
            for (property in data[i]) 
            {
                li = document.createElement("li");
                if (property === "appointed") 
                {
                    var btn = document.createElement("button");
                    if (data[i][property] === true) 
                    {
                        count += 1;
                        btn.innerHTML = "已签到";
                    }
                    else  btn.innerHTML = "确定";
                    btn.setAttribute("class", "dst-user-appointed");
                    li.appendChild(btn);
                }
                else li.innerHTML = data[i][property];
                ul.appendChild(li);
            }

            user.appendChild(ul);
        }

        all = document.createElement("div");

        ul = document.createElement("ul");
        li = document.createElement("li");
        li.innerHTML = "预约总人数: " + length;
        ul.appendChild(li);
        li = document.createElement("li");
        li.innerHTML = "剩余座位: " + (1000 - length);
        ul.appendChild(li);
        li = document.createElement("li");
        li.innerHTML = "签到率: " + count / length * 100 + "%";
        ul.appendChild(li);
        all.appendChild(ul);

        document.getElementById(target).innerHTML = user.outerHTML;
        document.getElementById(end).innerHTML = all.outerHTML;
    }

    //events
    onClick();

    //attach to global window object
    global.dycalendar = dycalendar;

}(typeof window !== "undefined" ? window : this));
