import React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import "./App.css";

import Discussion from "./components/Discussion";

import dark from "./themes/dark";
import light from "./themes/light";

const postsDummy = ["2o3iupoweuqo", "2o32o467o3y364", "2o32o46sdaf7o3y364"];

const postUnits = {
	"2o3iupoweuqo": {
		created_at: "2020-10-06T02:28:52.000Z",
		author: "Christian",
		pith:
			"Project Xanadu was pretty interesting, we should include it in the list too.",
	},
	"2o32o467o3y364": {
		created_at: "2020-10-06T02:36:31.000Z",
		author: "Sam",
		pith:
			"We <em>might</em> be able to try out one of the old Xanadu prototypes.",
	},
	"2o32o46sdaf7o3y364": {
		created_at: "2020-10-06T04:41:45.000Z",
		author: "Jimmy",
		pith:
			"<cite>2o3iupoweuqo</cite> I went ahead and added Xanadu, and this <cite>2o32o467o3y364</cite> would be awesome. ",
	},
};

const documentDummy = {
	pith:
		"Project Xanadu was the first hypertext project, and aimed to link the world's information digitally",
	ancestors: [
		{
			unit_id: "28utwejf9pq348ut",
			pith: "Some existing hypertext projects to use as inspiration",
		},
		{
			unit_id: "8934tyhgpwehgqqh",
			pith: "Inspiration for the new project",
		},
		{ unit_id: "a2rqghaehrhgoaer", pith: "10/11/20" },
		{ unit_id: "3ytq384hgwaegehg", pith: "Meetings" },
	],
	unit_id: "28utwejf9pq348ut",
	children: [
		{
			unit_id: "3498tyqe9ygq93g",
			pith:
				"Xanadu doesn't rely on the same paper metaphor that most digital publishing does today.",
			children: [
				{
					unit_id: "34utqpieorghpq34",
					pith:
						"Each document is composed of a series of transclusions to other documents.",
				},
				{
					unit_id: "1348qefioqph43uqgh",
					pith: "The links between documents are made visible.",
				},
			],
		},
		{
			unit_id: "3849t7093ygwe",
			pith:
				"Xanadu is often compared to Vannevar Bush's <em>Memex</em> <cite>2o32o467o3y364</cite>, a fictional machine allowing a user to index and traverse a repository of information.",
			children: [],
		},
		{
			unit_id: "3948yu9qhrgweg",
			pith:
				"A number of working prototypes of the Xanadu technology exist today.",
			children: [],
		},
	],
};

const usersDummy = [
	{
		user_id: "a4tuqpirghiquehg",
		nickname: "Christian",
		cursor_position: { unit_id: "p2o438tuioweh", position: -1 },
		active: true,
	},
	{
		user_id: "38tyierhfqp9348",
		nickname: "Sydney",
		cursor_position: { unit_id: "p2o438tuioweh", position: -1 },
		active: false,
	},
];

const timelineDummy = [
	// {
	// 	unit_id: "2o32o467o3y364",
	// 	start_time: "2020-10-06T02:28:52.000Z",
	// 	end_time: "2020-10-08T02:28:52.000Z",
	// }, // 2 days
	{
		unit_id: "3849t7093ygwe",
		pith:
			"Xanadu is often compared to Vannevar Bush's <em>Memex</em> <cite>2o32o467o3y364</cite>, a fictional machine allowing a user to index and traverse a repository of information.",
		start_time: "2020-10-06T02:27:52.000Z",
		end_time: "2020-10-06T02:29:52.000Z",
	}, // 2 min
	{
		unit_id: "3948yu9qhrgweg",
		pith:
			"A number of working prototypes of the Xanadu technology exist today.",
		start_time: "2020-10-08T02:28:45.000Z",
		end_time: "2020-10-08T02:29:00.000Z",
	}, // 45 sec
	{
		unit_id: "34utqpieorghpq34",
		pith:
			"Each document is composed of a series of transclusions to other documents.",
		start_time: "2020-10-08T02:29:00.000Z",
		end_time: "2020-10-08T02:29:15.000Z",
	}, // 15 sec
	{
		unit_id: "1348qefioqph43uqgh",
		pith: "The links between documents are made visible.",
		start_time: "2020-10-08T02:29:00.000Z",
		end_time: "2020-10-08T02:29:01.000Z",
	}, // 15 sec
];

function App() {
	const storedDarkMode = localStorage.getItem("darkModeActive");
	const [darkModeActive, setDarkModeActive] = useState(storedDarkMode);

	let theme;

	if (darkModeActive !== null) {
		theme = darkModeActive ? dark : light;
	} else {
		if (window.matchMedia("(prefers-color-scheme: light)").matches) {
			theme = light;
		} else theme = dark; // default to dark mode
	}

	console.log(theme);
	return (
		<div className="App">
			<ThemeProvider theme={theme}>
				<Discussion
					setDarkMode={(val) => setDarkModeActive(val)}
					timeline={timelineDummy}
					content={postUnits}
					posts={postsDummy}
					document={documentDummy}
					users={usersDummy}
				/>
			</ThemeProvider>

			{/*<Router>
				<Switch>
					<Route
						exact
						path="/b/:boardID/d/:discussionID"
						component={Discussion}
					/>
					<Route exact path="/b/:boardID" component={Board} />
				</Switch>
			</Router>*/}
		</div>
	);
}

export default App;
