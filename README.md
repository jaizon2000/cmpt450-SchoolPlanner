# README.md

###### 🔗 Useful links

[Dash Callbacks](https://dash.plotly.com/basic-callbacks#dash-app-state) 

[Filtering Data Tables](https://dash.plotly.com/datatable/callbacks) 

###### 📑 Documentation Links

[Plotly Dash](https://dash.plotly.com/) 

[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) 

[Pandas](http://pandas.pydata.org/docs/user_guide/10min.html) 

## Inputs Column
### Search courses

#### Output

`collapse-card-{i}` on its `style` 

`courses-results-container` - 

#### Input

`course-search-input` - 

#### State

### Card Toggles

#### Output

`collapse-#` - collapse tab

#### Input

`group=#-toggle` - card group toggle

`*args*` Having an [unknown number of arguments](https://bit.ly/3syoB0Z), [link 2](https://bit.ly/3fr7Kt9)

#### State

`collapse-#` - collapse tab

------

### Dropdown Multiselect

#### Output

`table` - student’s table

#### Input

`courses-input` - multiselect dropdown

#### State

**[States](https://bit.ly/3uePXK9) allow user to input before running the main action**

So instead of getting the input as soon as there’s a change, the input is only gotten when the `Input` is triggered.

`status-radio` - status of selected courses

`add-to-planner-btn` - button to add to table

- The `Inputs` in `@app.callback` 
  - the action function parameters (function below below `@app.callback`) are in the order of the input in `@app.callback`.

## Data Table & Sunburst Column

- [ ] Export current data table
- [ ] Import a data table (csv, json)

### Data table

data table changes -> change checklist



## Checklist Column

[Dash Bootstrap Checklist Input](https://bit.ly/3sDJ8Bk) 

### change in checklist -> change data table

[Getting labels and values of checklist](https://community.plotly.com/t/dcc-dropdown-using-selected-label-in-callback-not-value/22003/9) 

#### Output

`my-table` - 

#### Input

`checklist-input-0` - 

`checklist` - 

#### ~~State~~