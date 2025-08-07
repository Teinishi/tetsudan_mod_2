function clamp(x, a, b)
	return math.min(math.max(x, a), b)
end

function lerp(a, b, t)
	return a*(1 - t) + b*t
end

local smooth = true
local t = 1
local up = nil
local show_mesh1 = false
local transform0, transform1 = matrix.identity(), matrix.identity()

function update(inserted, t_tgt)
	if inserted and t == t_tgt then
		smooth = false
	elseif not inserted then
		smooth = true
	end
	t_tgt = (not inserted or up > 1e-5) and 0.9 or t_tgt
	t = smooth and clamp(t_tgt, t - 0.05, t + 0.05) or t_tgt
	local up_tgt = (not inserted and math.abs(t - 0.9) < 1e-5) and 1 or 0
	up = up and clamp(up_tgt, up - 0.1, up + 0.1) or up_tgt
	local theta = lerp(90, -60, t)/180*math.pi
	transform0 = matrix.rotationY(theta)
	transform1 = matrix.multiply(transform0, matrix.translation(0, 0.1*up, 0))
end

function onParse()
	t, _ = parser.parseNumber("t", t)
	update(t)
end

function onTick()
	local composite, success = component.getInputLogicSlotComposite(0)
	if success then
		local inserted = composite.bool_values[1]
		local value = composite.float_values[1]
		update(inserted, clamp(value, 0, 1))
	end
end

function onRender()
	component.renderMesh0(transform0)
	if up ~= nil and up < 0.99 then
		component.renderMesh1(transform1)
	end
end
