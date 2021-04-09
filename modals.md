# Importing Modal

`import-modal`

`open-import` , `close-import`

The supported files you can export is `.csv` and `.xls.`

You ***must*** follow this column format (this means column name is ***case sensitive*** )

The only required cell to input is `Course ID` but it’s recommended to add a status!

Columns `Course Name`, `Credits`, and `Prerequisites` are automatically filled based on the given `Course ID`


| Course ID | Course Name | Credits | Prerequisites | Status  |
| --------- | ----------- | ------- | ------------- | ------- |
| CMPT 103  | --          | --      | --            | PLANNED |

Below is the raw `.csv` file of the example table above.

```
Course ID,Course Name,Credits,Prerequisites,Status
CMPT 101,,,PLANNED,
```



# Intro Modal

`intro-modal`

`open-intro`, `close-intro`

There are **3 columns**: *Find Courses*, *My Table*, and *Checklist*

1. **Find Courses**

   Here you can search for a course’s full description quickly.
   You can search by a course id, course name and, even by a course’s description. As you search, results will update live.

   ![](https://i.imgur.com/rtAsbTD.png) 

   You can select multiple courses and set a status for them. You can also remove them from the table.
   You can choose to import a `csv` or `xls` file to put data into your table. ***Check How to Import for more details*** 

   ![](https://i.imgur.com/h6koO6e.png?1)

   In the future, you will be able to switch to a sunburst view, showing the relation of courses in your table more visually. For now we’ll have to stick with the table 😅.

2. **My Table**

   This table represents your Computer Science Major degree plan.
   Every time you make changes from the ***Mark selected courses(s) as:*** section, it will be added to you table.
   You can export your table at any point into a `.csv` fille.

   Within the table, you can filter the data. You can filter by string or number, depending on the column.

   ![](https://i.imgur.com/Q9g4VFR.png) 

   The official docs on filtering tables can be found [here](https://bit.ly/31tUrjG).

   **Text & String Filtering**

   - `United`
   - `= United`
   - `United States`
   - `"United States"`
   - `= United States`
   - `= "United States"`
   - `> United`
   - `>= United`
   - `< United`	
   - `<= United`

   **Numeric Filtering**

   - `43.828`
   - `= 43.828`
   - `> 43.828`
   - `>= 43.828`
   - `< 43.828`
   - `<= 43.828`

   Below the table, are where you can go back to this window if you ever get lost. You can also find helpful information here like ***How to Import***.

3. **Checklist**

   Finally, the checklist. The dropdown allows you to change your checklist requirements based on the stream you choose.

   The default stream is the *Gaming Stream*.

   ![](https://i.imgur.com/rXgKu7e.png) 

   In the future, any updates to your table will be able to reflect on you checklist.



# How to read prerequisites

`readpre-modal`

`open-readpre`, `close-readpre`

A prerequisite of a course is always wrapped in **brackets**.

If there are no prerequisites = `()`

If there’s one or more prerequisites = `(CMPT 201, CMPT 103, ...)`

Inside the brackets, courses can be enclosed in **square brackets** `[CMPT 200, 201]`

This means that the prerequisite is choosing one of those courses in the list.

###### An Example (CMPT 272)

To understand more, let’s use `CMPT 272` as an example.

Its prerequisites are: `([CMPT 101, CMPT 103, CMPT 200], MATH 114, [MATH 120, MATH 125])`

The whole prerequisite is **enclosed in brackets**, meaning that we **must take all the courses inside the brackets**.

Let’s go through each element in the brackets:

- `[CMPT 101, CMPT 103, CMPT 200]` - Take `CMPT 101` or `CMPT 103` or `CMPT 200`
- `MATH 114` - Take MATH 114
- `[MATH 120, MATH 125]` - Take `MATH 120` or `MATH 125`

##### That’s it! Now you know how to fully read prerequisites.

In the future, we hope to make this more visual!