-- include sfx 0 "m_tns_tetsudan_controller_1.ogg"
-- include sfx 1 "m_tns_tetsudan_controller_2.ogg"

local PIVOT = {0, 0.029167, -0.125}
local STEP_ANGLES = {33, 21, 11, 4, -3, -9, -15, -21, -29, -36, -46, -56, -66}
local STEP_START = -8

local mat_pivot = matrix.translation(PIVOT[1], PIVOT[2], PIVOT[3])
local mat_pivot_neg = matrix.translation(-PIVOT[1], -PIVOT[2], -PIVOT[3])
local step_angles_rad = {}
for i, v in ipairs(STEP_ANGLES) do
	step_angles_rad[STEP_START + i - 1] = math.rad(v)
end

function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local pos = nil
local theta = nil
local transform = matrix.identity()

function update(npos)
	if npos == nil then return end
	pos = npos
	local theta_tgt = step_angles_rad[pos]
	if theta_tgt == nil or theta == theta_tgt then return end
	if theta == nil or math.abs(theta_tgt - theta) < 1e-4 then
		theta = theta_tgt
	else
		theta = lerp(theta, theta_tgt, 0.4)
	end
	transform = matrix.multiply(matrix.rotationX(theta), mat_pivot_neg)
	transform = matrix.multiply(mat_pivot, transform)
end

function onTick()
	local value, success = component.getInputLogicSlotFloat(0)
	if success then
		local npos = clamp(math.floor(value + 0.5), STEP_START, STEP_START + #STEP_ANGLES - 1)
		if pos ~= nil and npos ~= pos then
			if npos == 0 or npos == STEP_START then
				component.sfxPlayOnce(1, 1, 0, 0, 0, 1, 6, 1, 1, 0.5)
			end
			component.sfxPlayOnce(0, 0, 0, 0, 0, 1, 6, 1, 1, 0.5)
		end
		update(npos)
	end
end

function onRender()
	component.renderMesh0(transform)
end
